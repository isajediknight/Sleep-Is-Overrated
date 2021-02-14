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

    def middle_zero(self,number):
        """
        Aligns the '.' to be in the middle of self.total_spaces

        ie:
               123.456789
                 0.032324
          32113123.777
                 3.00000002
        """

        if type(number) == type(0):
            before_decimal = self.total_spaces - len(str(number))
            after_decimal = 0
            return " " * before_decimal + str(number)
        else:
            zero_loc = str(number).find('.')
            before_decimal = int(self.total_spaces) - zero_loc
            # make this 8 because 8 is the numbers zeros BTC goes down to
            after_decimal = 9 - len(str(number)[zero_loc:])#int(self.total_spaces / 2) - (zero_loc + 1)
            # if not divisible by 2 then add it to the after_decimal so it is not lost
            if self.total_spaces % 2 != 0:
                after_decimal += 1

            message = " " * before_decimal
            message += str(int(float(number)))
            message += str(number)[zero_loc:]
            message += after_decimal * " "

            return message

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

        