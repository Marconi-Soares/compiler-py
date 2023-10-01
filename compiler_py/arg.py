# import argparse
# 
# # Create an argument parser
# parser = argparse.ArgumentParser(description='Process some integers.')
# 
# # Add arguments and options to the parser
# parser.add_argument('-n', '--name', help='The name of the person to greet.')
# parser.add_argument('--verbose', '-v', action='store_true', help='Print verbose output.')
# parser.add_argument('numbers', type=int, nargs='*', help='The numbers to process.')
# 
# # Parse the command line arguments
# args = parser.parse_args()
# 
# # Process the arguments
# if args.verbose:
#     print('Verbose output enabled.')
# 
# if args.name:
#     print(f'Hello, {args.name}!')
# 
# if args.numbers:
#     print(f'The sum of the numbers is {sum(args.numbers)}.')