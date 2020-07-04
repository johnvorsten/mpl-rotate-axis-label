# Dynamically rotate axis labels in matplotlib

3D plots have (3) axis'.  We have the ability to set tick positions and labels for each axis using the (axis3d)[https://matplotlib.org/api/_as_gen/mpl_toolkits.mplot3d.axis3d.Axis.html#mpl-toolkits-mplot3d-axis3d-axis] toolkit in matplot lib.  The API calls would go something like `axes.xaxis.set_xticklabels(['a','b']).  

Fortunately, there is great control over how those labels are displayed in matplotlib.  We can set rotation, vertical alignment, and horizontal alignment relative to the viewers fixed screen coordinate system like : 

```python
fig3d = plt.figure(1)
ax3d = fig3d.add_subplot(111, projection='3d')
ax3d.set_title('Axes Title')
ax3d.set_ylim(0,2)

# Label X axis
ax3d.set_xticks([1])
ax3d.set_xticklabels(['Non-rotated Label\n"left,top"'])
ax3d.xaxis.get_majorticklabels()[0].set_verticalalignment('top')
ax3d.xaxis.get_majorticklabels()[0].set_horizontalalignment('left')
# ax3d.xaxis.get_majorticklabels()[0].set_rotation(0)
# Label y axis
ax3d.set_yticks([1])
ax3d.set_yticklabels(['Rotated Label'])
ax3d.yaxis.get_majorticklabels()[0].set_rotation(45)

# Label axis
ax3d.set_xlabel('X Axis', labelpad=20)
ax3d.set_ylabel('Y Axis', labelpad=20)
```

![Rotated Label](https://github.com/johnvorsten/mpl-rotate-axis-label/blob/master/Rotate_Example.png)

But what if we want to continuously align a label to its respective axis? There is no way to anchor / redraw axis labels to continuously align them to an axis.  The default behavior to to set their rotation relative to the computer screen.  A solution is to use event signals to redraw axis labels.  Here is an example : 

![Aligned Label](https://github.com/johnvorsten/mpl-rotate-axis-label/blob/master/Example.png)

See the code for the full slot method and how to connect it to a figures 'draw-event'.