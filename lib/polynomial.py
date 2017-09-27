import re


class Polynomial:
    def __init__(self, polynomial):
        self._polynom = polynomial.replace(' ', '')
        self.errors = ''
        self._variables = list(set(re.findall(r'[a-zA-Z]', polynomial)))
        self._variables.sort()
        self._dict = {}
        self._variable_degree_dict = {x: '' for x in self._variables}

    def __eq__(self, other):
        return self.is_equal(other) and other.is_equal(self)

    def __str__(self):
        return self._polynom



    def is_equal(self, other):
        parsed1 = self.split_polynom_to_dict()
        parsed2 = other.split_polynom_to_dict()
        for degree in parsed1:
            value = parsed1[degree]
            if value == 0:
                continue
            if degree not in parsed2 or value != parsed2[degree]:
                return False
        return True

    def is_correct(self):
        unacceptable = re.findall(r'[^a-zA-Z\d\-+*^()]', self._polynom)
        if not unacceptable.__len__() == 0:
            self.errors = 'unacceptable symbols: '+' '.join(x for x in unacceptable)
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
        monomials = filter(None, self._polynom.split('+'))
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
                    if index == len(monom) - 1:
                        variable_degree_dict[variable] = 1
                else:
                    variable_degree_dict['_'] += e
            elif index == len(monom) - 1:
                if e.isalpha():
                    variable_degree_dict[variable] = degree if not degree == '' else '1'
                    variable_degree_dict[e] = '1'
                else:
                    degree += e
                    variable_degree_dict[variable] = degree
                    degree = ''
            elif e.isalpha():
                variable_degree_dict[variable] = degree
                variable = e
                degree = ''
            else:
                degree += e
        if variable_degree_dict['_'] == '':
            variable_degree_dict['_'] = '1'
        elif variable_degree_dict['_'] == '-':
            variable_degree_dict['_'] = '-1'
        return variable_degree_dict

    def __mul__(self, other):
        # не могу в нормальное перемножение как ни крути
        parsed1 = self.split_polynom_to_dict()
        parsed2 = other.split_polynom_to_dict()
        result = {}

        for degrees_tuple1 in parsed1:
            for degrees_tuple2 in parsed2:
                multiplier = parsed1[degrees_tuple1] * parsed2[degrees_tuple2]

                degrees = tuple(degree1 + degree2
                                for index1, degree1 in enumerate(degrees_tuple1)
                                for index2, degree2 in enumerate(degrees_tuple2)
                                if index1 == index2)
                if degrees in result:
                    result[degrees] += multiplier
                else:
                    result[degrees] = multiplier
        return result