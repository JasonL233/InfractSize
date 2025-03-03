import os
import cv2
import numpy as np
import torch

WIDTH = 256
HEIGHT = 256
IMG_SIZE = (HEIGHT, WIDTH)

## HMRI Image Segmentation Project custom dataset class

## Pass in two masks: One is the target area, one is the (total area - cavity)

class SegmentationDataset():

  # Constructor
  def __init__(self, root, ids, transform=None):
    self.root = root
    self.ids = ids
    self.transform = transform

    # load all image files, sorting them to ensure they are all aligned
    self.image_dir = os.path.join(root, "images")
    self.target_mask_dir = os.path.join(root, "targetMasks")
    self.total_mask_dir = os.path.join(root, "totalMasks")

    # Filter out '.ipynb_checkpoints' and non-file entries
    self.imgs = sorted([
            f for f in os.listdir(self.image_dir)
            if os.path.isfile(os.path.join(self.image_dir, f))
        ])
    
  # Return the size of the dataset
  def __len__(self):
    return len(self.imgs)


  def __getitem__(self, index):
    filename = self.ids[index]

    # Load images and masks
    image_path = os.path.join(self.image_dir, filename)
    target_mask_path = os.path.join(self.target_mask_dir, f"targetMask{filename}")
    total_mask_path = os.path.join(self.total_mask_dir, f"totalMask{filename}")

    print(image_path)
    print(target_mask_path)
    print(total_mask_path)

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    img = img[:, :, 0:3]

    # Load the target and total masks
    target_area = cv2.imread(target_mask_path, cv2.IMREAD_GRAYSCALE)
    total_area = cv2.imread(total_mask_path, cv2.IMREAD_GRAYSCALE)

    # Check if the masks were loaded correctly
    if target_area is None:
      raise FileNotFoundError(f"Target mask not found at path: {target_mask_path}")
    if total_area is None:
      raise FileNotFoundError(f"Total mask not found at path: {total_mask_path}")

    # Resize both masks to match the dimensions of the image
    target_area_resized = cv2.resize(target_area, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
    total_area_resized = cv2.resize(total_area, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Continue with further processing (e.g., extracting unique values, creating masks, etc.)
    tar_unique = np.unique(target_area_resized)
    tar_unique = tar_unique[tar_unique != 0]
    tot_unique = np.unique(total_area_resized)
    tot_unique = tot_unique[tot_unique != 0]

    # Initialize empty masks array to hold 6 separate masks
    target_masks = np.zeros((3, img.shape[0], img.shape[1]), dtype=np.uint8)
    total_masks = np.zeros((3, img.shape[0], img.shape[1]), dtype=np.uint8)

    # Fill each mask based on unique values in the combined-mask
    for i in range(3):
      if i < len(tar_unique):
        target_masks[i] = (target_area_resized == (i + 1)).astype(np.uint8)
      else:
        target_masks[i] = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

      if i < len(tot_unique):
        total_masks[i] = (total_area_resized == (i + 1)).astype(np.uint8)
      else:
        total_masks[i] = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

    # Resize the masks to the desired size if needed
    target_masks = [cv2.resize(mask, IMG_SIZE, cv2.INTER_NEAREST) for mask in target_masks]
    total_masks = [cv2.resize(mask, IMG_SIZE, cv2.INTER_NEAREST) for mask in total_masks]

    # Concatenate masks
    masks = np.concatenate((target_masks, total_masks), axis=0)

    # Get bounding box for each mask
    num_objs = masks.shape[0]
    boxes = torch.zeros([num_objs, 4], dtype=torch.float32)  # 4 represent x_min, x_max, y_min, y_max
    for i in range(num_objs):
      x, y, w, h = cv2.boundingRect(masks[i])
      if w == 0.0 and h == 0.0:
        x, y, w, h = 31, 31, 1, 1
      boxes[i] = torch.tensor([x, y, x + w, y + h])

    # Masks transform
    masks = torch.as_tensor(np.array(masks), dtype=torch.uint8)

    # Image transform
    img = cv2.resize(img, IMG_SIZE, cv2.INTER_NEAREST)
    img = torch.as_tensor(np.array(img), dtype=torch.float32)
    img = img.swapaxes(0, 2).swapaxes(1, 2)  # Convert from HWC to CHW

    # Create labels to differentiate the target area and the (total area - cavity)
    labels = torch.tensor([1 if i < 3 else 2 for i in range(6)], dtype=torch.int64)

    target = {
      "boxes": boxes,
      "labels": labels,
      "masks": masks,
    }

    return img, target, filename

