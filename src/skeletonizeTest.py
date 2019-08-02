from skimage.morphology import skeletonize
import matplotlib.pyplot as plt
from skimage.util import invert
from skimage import io
from skimage import color
from skimage import img_as_float
from src import RoadMap as RM

# Invert the image
image = invert(io.imread('M2.png', as_gray=True))

# perform skeletonization
image = image > 0
skeleton = skeletonize(image)
skeleton_disp = color.gray2rgb(img_as_float(skeleton))

for i in RM.RoadMap.find_intersections(skeleton):
    skeleton_disp[i[0]][i[1]] = skeleton_disp[i[0]][i[1]] * [1, 0, 0]
# display results
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                         sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(skeleton_disp, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

fig.tight_layout()
plt.show()
