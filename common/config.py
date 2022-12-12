from configobj import ConfigObj


LAB = True
if LAB == True :
    config_file = "/opt/selena/config.ini"

def load_config(config_file):

    config = ConfigObj(config_file, list_values=True)
    return config

if __name__ == '__main__':
    config = load_config(config_file)
    print (config)