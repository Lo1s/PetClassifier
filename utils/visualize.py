import torch
import matplotlib.pyplot as plt
import numpy as np


def visualize_model(model, dataloaders, class_names, device, num_images=6):
    was_training = model.training
    model.eval()
    images_so_far = 0
    fig = plt.figure()

    with torch.no_grad():
        for i, sample in enumerate(dataloaders['val']):
            # computation to GPU
            image = sample["image"]
            label = sample["label"]

            data = image.to(device=device, dtype=torch.float)
            targets = label.to(device)

            outputs = model(data)
            _, preds = torch.max(outputs, 1)

            for j in range(data.size()[0]):
                images_so_far += 1
                ax = plt.subplot(num_images // 2, 2, images_so_far)
                ax.axis('off')
                ax.set_title('predicted: {}'.format(class_names[preds[j]]))
                imshow(data.cpu().data[j])

                if images_so_far == num_images:
                    model.train(mode=was_training)
                    return

            model.train(mode=was_training)


def imshow(inp, title=None):
    """Imshow for Tensor."""
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated

