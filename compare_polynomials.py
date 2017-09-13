import sys
import argparse
from polynomial import Polynomial


def parse_args():
    parser = argparse.ArgumentParser(
        usage='%(prog)s -p [polynom1] [polynom2]',
        description='The program takes two polynomials from console input with key \'-p\' or \'--polynoms\''
                    'and return if they are equal or not. '
                    'If you have a mistake in input polynoms it returns an error and description of mistake.',
        epilog='Exit codes description in the documentation.'
    )
    parser.add_argument("-p", "--polynoms", type=str, nargs='+',
                        help="Polynomials to compare")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.polynoms is None:
        sys.stdout.write("You should enter two polynoms to compare")
        sys.exit(1)
    if not len(args.polynoms) == 2:
        sys.stdout.write('You should give program two arguments = two polynomials')
        sys.exit(1)
    polynomial1 = Polynomial(args.polynoms[0])
    polynomial2 = Polynomial(args.polynoms[1])
    if not polynomial1.is_correct() or not polynomial2.is_correct():
        sys.stdout.write("Polynomial is not in the right form! "
                         "\nYou have problem with {}. Check input again"
                         "\nRight form is the sum of classic monomials. "
                         "\nFor example, '2x^2+y^6*x^3' is in the right form."
                         "\nMonomial is also a polynomial for this program."
                         .
                         format(polynomial1.errors + polynomial2.errors))
        sys.exit(1)

    sys.stdout.write('Polynomials are equal' if polynomial1.is_equal(polynomial2)
                     else 'Polynomials are not equal')

if __name__ == '__main__':
    main()
