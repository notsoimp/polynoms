import re


class Polynomial:
    def __init__(self, polynom):
        self._polynom = polynom.replace(' ', '')
        self.errors = ''
        self._variables = list(set(re.findall(r'[a-zA-Z]', polynom)))
        self._variables.sort()
        self._dict = {}
        self._variable_degree_dict = {x: '' for x in self._variables}

    def is_correct(self):
        unacceptables = re.findall(r'[^a-zA-Z\d\-+*^()]', self._polynom)
        if not unacceptables.__len__() == 0:
            self.errors = 'unacceptable symbols: '+' '.join(x for x in unacceptables)
            return False
        pre_hats = re.findall(r'(?<![a-zA-Z])\^', self._polynom)
        if not pre_hats.__len__() == 0:
            self.errors = 'strange symbol before \"^\". ' \
                           '\nRemember that I can not build a number to the power'
            return False
        after_hats = re.findall(r'\^(?!\d)', self._polynom)
        if not after_hats.__len__() == 0:
            self.errors = 'strange symbol after \"^\".' \
                           '\nRemember that I can work only with natural degrees'
            return False
        open_brace = re.findall(r'[(]', self._polynom)
        close_brace = re.findall(r'[)]', self._polynom)
        if len(open_brace) != len(close_brace):
            self.errors = 'opened and closed braces'
            return False
        return True

    def split_polynom_to_dict(self):
        self._polynom = self._polynom.replace('-', '+-')
        monomials = self._polynom.split('+')
        for monom in monomials:
            variable_degree_dict = self.init_var_deg_dict(monom)
            for var in self._variables:
                if variable_degree_dict[var] == '':
                    variable_degree_dict[var] = 0
                variable_degree_dict[var] = int(variable_degree_dict[var])
            variable_degree_dict['_'] = int(variable_degree_dict['_'])
            degrees_tup = tuple(variable_degree_dict[e] for e in self._variables)
            if self._dict.get(degrees_tup) is None:
                self._dict[degrees_tup] = variable_degree_dict['_']
            else:
                self._dict[degrees_tup] += variable_degree_dict['_']
        return self._dict

    def init_var_deg_dict(self, monom):
        variable_degree_dict = {x: '' for x in self._variables}
        variable = ''
        degree = ''
        variable_degree_dict['_'] = ''
        for index, e in enumerate(monom):
            if e == '*' or e == '^':
                continue
            if variable == '':
                if e.isalpha():
                    variable = e
                    if variable_degree_dict['_'] == '':
                        variable_degree_dict['_'] = '1'
                    elif variable_degree_dict['_'] == '-':
                        variable_degree_dict['_'] = '-1'
                else:
                    variable_degree_dict['_'] += e
            elif index == len(monom) - 1:
                if e.isalpha():
                    variable_degree_dict[variable] = degree if not degree == '' else '1'
                    variable_degree_dict[e] = '1'
                elif e.isdigit():
                    degree += e
                    variable_degree_dict[variable] = degree
                    degree = ''
            elif e.isalpha():
                if degree == '':
                    degree = '1'
                variable_degree_dict[variable] = degree
                variable = e
                degree = ''
            else:
                degree += e
        return variable_degree_dict

    def is_equal(self, other):
        parsed1 = self.split_polynom_to_dict()
        parsed2 = other.split_polynom_to_dict()
        return parsed1 == parsed2


if __name__ == "__main__":
    polynom = Polynomial("2")
    polynom.init_var_deg_dict("2")
