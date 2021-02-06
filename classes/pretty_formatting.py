class PrettyFormatting:

    def __init__(self,total_spaces=5,up_color='green',down_color='red',unchanged_color='grey'):
        self.total_spaces = total_spaces
        self.up_color = up_color
        self.down_color = down_color
        self.unchanged_color = unchanged_color

    def set_up_color(self,up_color):
        self.up_color = up_color

    def set_down_color(self,down_color):
        self.down_color = down_color

    def set_unchanged_color(self,unchanged_color):
        self.unchanged_color = unchanged_color

    def add_spaces(self,number):
        new_string = str(number)
        spaces_to_add = self.total_spaces - len(str(number))

        if spaces_to_add > 0:
            return " " * spaces_to_add
        else:
            return ""

    def diff_two(self,old,new):
        """
        Returns a ColoredText object as a string with correct text color
        """

        #if type(value_1) == type(0) and type(value_2) == type(0)
        # for the moment lets assume these are BTC amounts as satoshis

        cc_color = self.up_color

        old_counter = 0
        for character in old:
            if character == '0' or character == '.':
                old_counter += 1
            else:
                break

        new_counter = 0
        for character in new:
            if character == '0' or character == '.':
                new_counter += 1
            else:
                break

        new_old = int(old[old_counter:])
        new_new = int(new[new_counter:])

        diff = new_old - new_new

        if diff > 0:
            cc_color = self.down_color
        elif diff == 0:
            cc_color = self.unchanged_color

        diff = abs(diff)

        return self.add_spaces(diff) + str(diff), cc_color