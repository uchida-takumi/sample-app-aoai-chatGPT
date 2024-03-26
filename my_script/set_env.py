# .env ファイルの環境変数をすべてdict型で取得
import os
from dotenv import dotenv_values

def set_env(type='azd', env_file='.env', app_name=None, resource_group_name=None, subscription_name=None):
        # .env ファイルの環境変数をすべて取得
        for k, v in dotenv_values(env_file).items():
            print(f"{k}={v}")
            if type == 'azd':
                if v:        
                    # sh で, azd env set {k} {v} を実行
                    command = f"azd env set {k} {v}"
                # 以下の az webapp config appsetting set は無意味かもしれない
                elif type == 'az':
                    command = "az webapp config appsettings set "
                    if app_name:
                        command += f"--name {app_name} "
                    if subscription_name:
                        command += f"--subscription {subscription_name} "
                    if resource_group_name:
                        command += f"--resource-group {resource_group_name} "
                    command += f"--settings {k}={v}"
                os.system(command)

if __name__ == "__main__":
     # parse arg
    import argparse
    parser = argparse.ArgumentParser()
    # type は defaultで azd にしておく
    parser.add_argument("--type", default="azd", help="azd or az")
    parser.add_argument("--env_file", default=".env", help="env file")
    parser.add_argument("--app_name", help="app name")
    parser.add_argument("--resource_group_name", help="resource group name")
    parser.add_argument("--subscription_name", help="subscription name")
    args = parser.parse_args()
    if not args.app_name:
        args.app_name = os.environ.get("APP_NAME")
    if not args.resource_group_name:
        args.resource_group_name = os.environ.get("RESOURCE_GROUP_NAME")
    if not args.subscription_name:
        args.subscription_name = os.environ.get("SUBSCRIPTION_NAME")
    print(args)
    set_env(type=args.type, env_file=args.env_file, app_name=args.app_name, resource_group_name=args.resource_group_name, subscription_name=args.subscription_name)
                      
