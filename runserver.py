from apps import create_apps


apps = create_apps()


if __name__ == '__main__':
    apps.run(host='0.0.0.0', port=80, debug=True)

