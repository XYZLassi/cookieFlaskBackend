#!/usr/bin/python
def main():
    from {{cookiecutter.package_name}}.ext import scheduler

    try:
        print('Start background Service')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        pass


if __name__ == '__main__':
    main()
