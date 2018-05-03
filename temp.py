from tkinter import ttk, font
import tkinter


class NavigationTree(object):
    """Generate the navigation tree view
    """
    def __init__(self, root: tkinter.Tk):
        font_linespace = font.Font(family='Consolas', size=12).metrics()['linespace'] + 2
        ttk.Style().configure('Navigation.Treeview', font=('Consolas', 12), rowheight=font_linespace)
        self._nav_tree = ttk.Treeview(root, style='Navigation.Treeview')

    def get_instance(self):
        index = 0
        self._add_mobike_branch(index)
        index += 1
        self._add_shanghaimetro_branch(index)
        index += 1
        self._add_crh_branch(index)
        index += 1
        self._add_flight_branch(index)
        return self._nav_tree

    def _add_mobike_branch(self, index):
        self._nav_tree.insert('', index=index, iid='mobike', text='Mobike')
        self._nav_tree.insert('mobike', index=0, iid='mobike.biketype', text='Bike types')
        self._nav_tree.insert('mobike', index=1, iid='mobike.bike', text='Bikes')
        self._nav_tree.insert('mobike', index=2, iid='mobike.snseg', text='SN segments')

    def _add_shanghaimetro_branch(self, index):
        self._nav_tree.insert('', index=index, iid='shanghaimetro', text='Shanghai Metro')
        self._nav_tree.insert('shanghaimetro', index=0, iid='shanghaimetro.traintype', text='Train types')
        self._nav_tree.insert('shanghaimetro', index=1, iid='shanghaimetro.train', text='Trains')
        self._nav_tree.insert('shanghaimetro', index=2, iid='shanghaimetro.trip', text='Trips')
        self._nav_tree.insert('shanghaimetro', index=3, iid='shanghaimetro.record', text='Add trips')

    def _add_crh_branch(self, index):
        pass

    def _add_flight_branch(self, index):
        pass


class LabelGrid(object):
    def __init__(self, root, num_rows, num_cols):
        self.size = (num_rows, num_cols)
        self.frame = ttk.Frame()
        self.labels = []
        self._make_label_grid()

    def _make_label_grid(self):
        for idx_row in range(self.size[0]):
            for idx_col in range(self.size[1]):
                label = ttk.Label(self.frame, text='NA', font=('Consolas', 12), anchor='center',
                                  background='white', borderwidth=2, relief='solid')
                label.grid(row=idx_row, column=idx_col, ipadx=5, ipady=5)
                self.labels.append(label)

    def get_label(self, row, col):
        return self.labels[row * self.size[1] + col]

    def get_instance(self):
        return self.frame


root = tkinter.Tk()
root.geometry('1920x1080')
font_linespace = font.Font(family='Consolas', size=12).metrics()['linespace'] + 2
ttk.Style().configure('Nav.TreeView', font=('Consolas', 12), rowheight=font_linespace)
tree_view = ttk.Treeview(root, style='Nav.Treeview')
tree_view.insert('', 0, 'mobike', text='Mobike')
tree_view.insert('mobike', index=0, iid='mobike.biketype', text='Bike types')
# tree_view.pack(fill='both', expand='yes')
tree_view.grid(row=0, column=0)

# nav_tree_maker = NavigationTree(root)
# nav_tree = nav_tree_maker.get_instance()
# nav_tree.pack()
#
# label_grid = LabelGrid(root, 10, 10)
# label_grid.get_instance().pack()


root.mainloop()
