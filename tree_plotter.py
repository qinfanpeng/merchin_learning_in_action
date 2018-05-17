import matplotlib.pyplot as plt
from common_utils import is_leaf

decision_node = dict(boxstyle='sawtooth', fc='0.8')
leaf_node = dict(boxstyle='round4', fc='0.8')
arrowprops = dict(arrowstyle='<-')


def plot_node(node_text, center_point, parent_point, node_type):
    create_plot.ax1.annotate(
        node_text,
        xy=parent_point,
        xytext=center_point,
        xycoords='axes fraction',
        textcoords='axes fraction',
        va='center',
        ha='center',
        bbox=node_type,
        arrowprops=arrowprops
    )


def get_leaf_count(tree):
    if is_leaf(tree): return 1

    root_key = tree.keys()[0]
    sub_tree = tree[root_key]
    if is_leaf(sub_tree): return 1

    def leaf_count_for(key):
        return 1 if is_leaf(sub_tree[key]) else get_leaf_count(sub_tree[key])

    # return reduce(lambda leaf_count, key: leaf_count + leaf_count_for(key), sub_tree.keys(), 0)
    return sum(map(lambda key: leaf_count_for(key), sub_tree.keys()))

def get_tree_depth(tree):
    if is_leaf(tree): return 1

    root_key = tree.keys()[0]
    sub_tree = tree[root_key]
    if is_leaf(sub_tree): return 1

    sub_tree_depths = map(lambda key: get_tree_depth(sub_tree[key]), sub_tree.keys())

    return max(sub_tree_depths) + 1


def plot_mid_text(center_point, parent_point, text):
    x_mid = (parent_point[0] - center_point[0]) / 2.0 + center_point[0]
    y_mid = (parent_point[1] - center_point[1]) / 2.0 + center_point[1]

    create_plot.ax1.text(x_mid, y_mid, text, va='center', ha='center', rotation=30)


def plot_tree(tree, parent_point, node_text):
    leaf_count = get_leaf_count(tree)
    root_key = tree.keys()[0]
    sub_tree = tree[root_key]

    center_point = (plot_tree.x_off + (1.0 + float(leaf_count)) / 2.0 / plot_tree.total_w, plot_tree.y_off)
    plot_mid_text(center_point, parent_point, node_text)

    plot_node(root_key, center_point, parent_point, decision_node)
    plot_tree.y_off = plot_tree.y_off - 1.0 / plot_tree.total_d

    for key in sub_tree.keys():
        if is_leaf(sub_tree[key]):
            plot_tree.x_off = plot_tree.x_off + 1.0 / plot_tree.total_w
            plot_node(sub_tree[key], (plot_tree.x_off, plot_tree.y_off), center_point, leaf_node)
            plot_mid_text((plot_tree.x_off, plot_tree.y_off), center_point, str(key))
        else:
            plot_tree(sub_tree[key], center_point, str(key))

    plot_tree.y_off = plot_tree.y_off + 1.0 / plot_tree.total_d


def create_plot(tree):
    figure = plt.figure(1, facecolor='white')
    figure.clf()

    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)

    plot_tree.total_w = float(get_leaf_count(tree))
    plot_tree.total_d = float(get_tree_depth(tree))
    plot_tree.x_off = -0.5 / plot_tree.total_w
    plot_tree.y_off = 1.0

    plot_tree(tree, (0.5, 1.0), '')

    plt.show()

# create_plot()
