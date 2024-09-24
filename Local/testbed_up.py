import docker
import os
import subprocess
import sys
import time
import argparse
import json

client = docker.from_env()
docker_images = client.images.list()

try: 
    def write_tag(tag):
        f = open('.env', 'a+')
        f.seek(0)
        contents = f.readlines()
        f.seek(0)
        f.truncate()
        for i, line in enumerate(contents): 
            if line[0:12] == 'LAUNCHER_TAG':
                contents[i] = f'LAUNCHER_TAG={tag}\n'
                f.writelines(contents)
                f.close()
                return
        f.writelines(contents + [f'LAUNCHER_TAG={tag}\n'])
        f.close()

    slash = os.path.sep
    root_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
    assets_subdir = os.path.join('Local', 'launcher-assets')
    agents_subdir = os.path.join('Agents')

    # bring up testbed
    templates_json_path = os.path.join(root_dir, assets_subdir, 'templates.json')
    with open(templates_json_path) as f:
        templates_data = json.load(f)
        templates_dict = {}
        for template in templates_data: 
            templates_dict[template['arg'][2:]] = template['services']

    services_json_path = os.path.join(root_dir, assets_subdir, 'services.json')
    with open(services_json_path) as f:
        services_data = json.load(f)

    agents_json_path = os.path.join(root_dir, assets_subdir, 'agents.json')
    with open(agents_json_path) as f:
        agents_data = json.load(f)
    parser = argparse.ArgumentParser(description='Pulls and starts testbed containers. Usage documented in Local/README_docker_build.md')
    subparsers = parser.add_subparsers(dest='subparser')
    template_parser = subparsers.add_parser('template', help="Choose a testbed template to launch")
    t_group = template_parser.add_mutually_exclusive_group(required=True)
    services_parser = subparsers.add_parser('services', help="Specify a group of services to run")
    agents_parser = subparsers.add_parser('agents', help="Specify an agent or agents to run")

    for template in templates_data:
        t_group.add_argument(template['abbrev'], template['arg'], action="store_true", help=template['display'])

    for service in services_data:
        services_parser.add_argument(service['abbrev'], service['arg'], action="store_true", help=service['display'])

    for agent in agents_data:
        agents_parser.add_argument(agent['abbrev'], agent['arg'], action="store_true", help=agent['display'])

    template_parser.add_argument('--tag', required=True, help="Specify a tag in the form of x.y.z-r")
    services_parser.add_argument('--tag', required=True, help="Specify a tag in the form of x.y.z-r")
    agents_parser.add_argument('--tag', required=True, help="Specify a tag in the form of x.y.z-r")


    args = parser.parse_args()
    tag = args.tag

    # build services_to_run, set of service names
    services_to_run = set()
    if args.subparser == 'template':
        args_dict = vars(args)
        template_name = None
        for key in args_dict.keys():
            if args_dict[key] == True:
                template_name = key
        if template_name: 
            service_names = templates_dict[template_name]
            for name in service_names:
                services_to_run.add(name)
    elif args.subparser == 'services' or args.subparser == 'agents':
        args_dict = vars(args)
        for key in args_dict.keys():
            if args_dict[key] == True:
                services_to_run.add(key)
    # launch core services
    if args.subparser == 'services' or args.subparser == 'template':
        print('Bringing up MQTT')
        dir = root_dir + slash + 'mqtt'
        os.chdir(dir)
        subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'pull'], shell=True, check=True)
        subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'up', '-d'], shell=True, check=True)
        print('Finished launching the MQTT, waiting for 5 seconds to ensure '\
                'everything works properly...')
        time.sleep(5)
        os.chdir(root_dir)
        if 'elk' in services_to_run:
            dir = root_dir + slash + 'ELK-Container'
            os.chdir(dir)
            write_tag(tag)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'pull'], shell=True, check=True)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'up', '-d'], shell=True, check=True)
            print('Finished launching the ELK stack, waiting for 5 seconds to ensure '\
                'everything works properly...')
            time.sleep(5)
            os.chdir(root_dir)
        if 'metadata' in services_to_run:
            dir = root_dir + slash + 'metadata' + slash + 'metadata-docker'
            os.chdir(dir)   
            write_tag(tag)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'pull'], shell=True, check=True)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'up', '-d'], shell=True, check=True)
            os.chdir(root_dir)

        if 'import_export' in services_to_run:
            print('Bringing up the Import/Export Dashboard')
            dir = root_dir + slash + 'metadata' + slash + 'metadata-web'
            os.chdir(dir)
            write_tag(tag)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'pull'], shell=True, check=True)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'up', '-d'], shell=True, check=True)
            os.chdir(root_dir)

        if 'minecraft' in services_to_run:
            print('Bringing up Minecraft')
            dir = root_dir + slash + 'Local'
            os.chdir(dir)
            write_tag(tag)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'pull'], shell=True, check=True)
            subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'up', '-d'], shell=True, check=True)
            os.chdir(root_dir)
            
        print('Testbed successfully launched')

    if args.subparser == 'agents':
        for agent in agents_data:
            if agent['arg'][2:] in services_to_run:
                print('Bringing up ', agent['name'])
                dir = root_dir + slash + 'Agents' + slash + agent['directory-name']
                os.chdir(dir)
                write_tag(tag)
                if os.path.exist("settings.env"):
                    subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', '--env-file', 'settings.env', 'pull'], shell=True, check=True)
                    subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', '--env-file', 'settings.env', 'up', '-d'], shell=True, check=True)
                else:
                    subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'pull'], shell=True, check=True)
                    subprocess.run(['docker-compose', '-f', 'docker-compose.launcher.yml', 'up', '-d'], shell=True, check=True)
                os.chdir(root_dir)

        print('Agents successfully launched')
except FileNotFoundError as ex:
    print('File not found: ' + ex.filename)
except AttributeError as ex:
    parser.print_help()
except SystemExit as ex:
    pass
except:
    info = sys.exc_info()
    type = info[0]
    ex = info[1]
    trace = info[2]
    print('Failed to launch testbed:', type, ex, trace)
finally:
    client.close()
