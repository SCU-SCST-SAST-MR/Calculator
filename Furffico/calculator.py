import argparse
parser = argparse.ArgumentParser(description='计算器')
parser.add_argument('mode',nargs='?',help='运行模式（cmd:命令行 basic:基础 adv:高级←默认）',default='adv')
args = parser.parse_args()

if args.mode=='cmd':
    from compute import main
elif args.mode=='basic':
    from basic import main
else:
    from advanced import main

main()