#!/usr/bin/env python
import argparse
import os
from datetime import datetime
from datetime import timedelta
from random import randint, shuffle
from subprocess import Popen
import sys


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]
        
    no_weekends = args.no_weekends
    frequency = args.frequency
    days_before = args.days_before
    
    if days_before < 0:
        sys.exit('days_before must not be negative')
    days_after = args.days_after
    if days_after < 0:
        sys.exit('days_after must not be negative')
        
    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    if user_name is not None:
        run(['git', 'config', 'user.name', user_name])

    if user_email is not None:
        run(['git', 'config', 'user.email', user_email])

    start_date = curr_date.replace(hour=20, minute=0) - timedelta(days_before)
    
    # --- NOUVELLE LOGIQUE ---
    # 1. Récupérer tous les jours valides (selon les week-ends et la fréquence)
    valid_days = []
    for n in range(days_before + days_after):
        day = start_date + timedelta(n)
        if (not no_weekends or day.weekday() < 5) and randint(0, 100) < frequency:
            valid_days.append(day)

    total_valid_days = len(valid_days)
    
    # Sécurité : vérifier qu'on a bien au moins 7 jours pour nos conditions spéciales
    if total_valid_days < 7:
        sys.exit('Erreur : pas assez de jours valides pour générer les 7 jours spéciaux.')

    # 2. Créer la liste exacte des commits : cinq '20', deux '13', et le reste à '4'
    commit_counts = [20] * 5 + [13] * 2 + [4] * (total_valid_days - 7)
    
    # 3. Mélanger la liste pour que ces jours spéciaux tombent au hasard
    shuffle(commit_counts)

    # 4. Effectuer les commits jour par jour
    for i, day in enumerate(valid_days):
        daily_commits = commit_counts[i]
        for m in range(daily_commits):
            commit_time = day + timedelta(minutes=m)
            contribute(commit_time)
    # --- FIN DE LA NOUVELLE LOGIQUE ---

    if repository is not None:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation ' +
          '\x1b[6;30;42mcompleted successfully\x1b[0m!')


def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date),
         '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])


def run(commands):
    Popen(commands).wait()


def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends',
                        required=False, action='store_true', default=False,
                        help="""do not commit on weekends""")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        required=False, help="""Ignoré avec la nouvelle logique personnalisée.""")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        required=False, help="""Percentage of days when the
                        script performs commits. If N is specified, the script
                        will commit N%% of days in a year. The default value
                        is 80.""")
    parser.add_argument('-r', '--repository', type=str, required=False,
                        help="""A link on an empty non-initialized remote git
                        repository. If specified, the script pushes the changes
                        to the repository. The link is accepted in SSH or HTTPS
                        format. For example: git@github.com:user/repo.git or
                        https://github.com/user/repo.git""")
    parser.add_argument('-un', '--user_name', type=str, required=False,
                        help="""Overrides user.name git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-ue', '--user_email', type=str, required=False,
                        help="""Overrides user.email git config.
                        If not specified, the global config is used.""")
    parser.add_argument('-db', '--days_before', type=int, default=365,
                        required=False, help="""Specifies the number of days
                        before the current date when the script will start
                        adding commits. For example: if it is set to 30 the
                        first commit date will be the current date minus 30
                        days.""")
    parser.add_argument('-da', '--days_after', type=int, default=0,
                        required=False, help="""Specifies the number of days
                        after the current date until which the script will be
                        adding commits. For example: if it is set to 30 the
                        last commit will be on a future date which is the
                        current date plus 30 days.""")
    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()