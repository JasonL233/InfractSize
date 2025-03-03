import os
import numpy as np
from torch.utils.data import DataLoader
from segmentationDataset import SegmentationDataset

BATCH_SIZE = 8

def collate_fn(batch):
  return tuple(zip(*batch))


def createDataset(root):
  ids = os.listdir(os.path.join(root, "images"))

  np.random.shuffle(ids)

  dataset = SegmentationDataset(root, ids)
  return dataset

# Create datasets
i_test_dataset = createDataset("../uploads/")

# Create dataloaders
i_test_dataloader = DataLoader(i_test_dataset, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)



# Debugging: Print first sample manually
print("Testing dataset loading...")
sample = i_test_dataset[0]  # Force __getitem__ call

img, target, filename = sample
print(f"Sample Filename: {filename}")
print(f"Image Shape: {img.shape}")
print(f"Target Keys: {target.keys()}")  # Should print 'boxes', 'labels', 'masks'

