import main

if __name__ == '__main__':
    # change this
    main.ros_node_setup()

    # Load configuration from environment variables or a config file

    main.app.run(host='0.0.0.0', port=5000,debug = True)
