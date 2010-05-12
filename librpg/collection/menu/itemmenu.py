from librpg.menu import Menu, Label, Cursor, Panel, VerticalScrollArea
from librpg.color import TRANSPARENT


class ExitLabel(Label):

    def __init__(self):
        Label.__init__(self, 'Exit')

    def activate(self):
        self.menu.close()
        return True


class ItemLabel(Label):

    def __init__(self, item, quantity, inventory):
        self.item = item
        self.quantity = quantity
        self.inventory = inventory
        s = self.create_string()
        Label.__init__(self, s)

    def activate(self):
        dialog = self.menu.create_action_dialog(self)
        dialog.sync_open()
        return True

    def refresh(self):
        self.quantity = self.inventory.get_amount(self.item)
        self.text = self.create_string()

    def create_string(self):
        return '%s x%d' % (self.item.name, self.quantity)


class ItemMenu(Menu):

    def __init__(self, inventory, party, width, height, x=0, y=0, theme=None,
                 bg=None, mouse_control=Menu.MOUSE_LOOSE):
        self.inventory = inventory
        self.party = party
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)

        self.exit_label = ExitLabel()
        self.add_widget(self.exit_label, (20, 12))

        self.inventory_panel = ItemScrollArea(self.inventory, self.width * 0.5,
                                              self.height - 50,
                                              24, (20, 10))
        self.add_widget(self.inventory_panel, (10, 40))
        
        cursor = Cursor()
        cursor.bind(self)

        self.config_action_dialog(100, 60, TRANSPARENT)

    def config_action_dialog(self, width=None, height=None, bg=None):
        if width is not None:
            self.action_dialog_width = width
        if height is not None:
            self.action_dialog_height = height
        self.action_dialog_bg = bg

    def create_action_dialog(self, item_label):
        x = (self.menu.inventory_panel.get_menu_position()[0]
             + self.menu.inventory_panel.width + 12) 
        y = self.menu.y + 12
        dialog = ActionDialog(self, item_label.item, item_label.quantity,
                              item_label,
                              self.action_dialog_width,
                              self.action_dialog_height, x, y,
                              theme=self.theme,
                              bg=self.action_dialog_bg)
        return dialog

    def remove_line(self, item):
        for i in xrange(len(self.inventory_panel)):
            if self.inventory_panel[i].get_contents()[0].item == item:
                self.inventory_panel.remove_line(i)
                break


class ItemScrollArea(VerticalScrollArea):
    
    def __init__(self, inventory, width, height, cell_height,
                 label_pos_inside_cell):
        VerticalScrollArea.__init__(self, width, height, cell_height)
        self.inventory = inventory
        
        ordered = inventory.get_ordered_list()
        amounts = inventory.get_items_with_amounts()
        pairs = [(item, amounts[item]) for item in ordered]
        for pair in pairs:
            item, qt = pair
            label = ItemLabel(item, qt, inventory)
            line = self.add_line()
            self[line].add_widget(label, label_pos_inside_cell)


# Action Dialog

class UseLabel(Label):

    def __init__(self, item, inv, party, item_label):
        Label.__init__(self, 'Use')
        self.item = item
        self.inv = inv
        self.party = party
        self.item_label = item_label

    def activate(self):
        print 'Used %s' % self.item.name
        self.item.use(self.party)
        self.inv.remove_item(self.item)
        if not self.inv.contains(self.item):
            self.menu.item_menu.remove_line(self.item)
            self.menu.close()
        else:
            self.item_label.refresh()
        return True

class TrashLabel(Label):

    def __init__(self, item, inv, item_label):
        Label.__init__(self, 'Trash')
        self.item = item
        self.inv = inv
        self.item_label = item_label

    def activate(self):
        print 'Trashed %s' % self.item.name
        self.inv.remove_item(self.item)
        if not self.inv.contains(self.item):
            self.menu.item_menu.remove_line(self.item)
            self.menu.close()
        else:
            self.item_label.refresh()
        return True


class ActionDialog(Menu):

    def __init__(self, item_menu, item, quantity, item_label, width, height,
                 x=0, y=0, theme=None, bg=TRANSPARENT,
                 mouse_control=Menu.MOUSE_LOOSE):
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)
        self.item_menu = item_menu

        self.item = item
        self.quantity = quantity

        self.panel = Panel(width, height)
        self.add_widget(self.panel, (0, 0))
        
        if hasattr(item, 'use'):
            self.use_label = UseLabel(self.item, self.item_menu.inventory,
                                      self.item_menu.party, item_label)
        else:
            self.use_label = TrashLabel(self.item, self.item_menu.inventory, 
                                        item_label)
        self.panel.add_widget(self.use_label, (20, 12))

        self.exit_label = ExitLabel()
        self.panel.add_widget(self.exit_label, (20, 36))

        cursor = Cursor()
        cursor.bind(self)
