# coding: utf-8

import os, sys
import ConfigParser
import click
from requests_oauthlib import OAuth1Session

APP_NAME = 'hiss'

def configure():
    click.echo('Setting up your auth information...')

    config = ConfigParser.RawConfigParser()
    config.add_section(APP_NAME)
    config.set(APP_NAME, 'PY_HISS_CONSUMER_KEY', click.prompt('Consumer Key', type=str))
    config.set(APP_NAME, 'PY_HISS_CONSUMER_KEY_SECRET', click.prompt('Consumer Secret', type=str))
    config.set(APP_NAME, 'PY_HISS_ACCESS_TOKEN', click.prompt('Access Token', type=str))
    config.set(APP_NAME, 'PY_HISS_ACCESS_TOKEN_SECRET', click.prompt('Access Token Secret', type=str))

    app_dir = click.get_app_dir(APP_NAME)
    if not os.path.exists(app_dir): os.makedirs(app_dir)

    path = os.path.join(app_dir, 'config.ini')
    with open(path, 'wb') as f:
        config.write(f)

    click.echo('Successfully configured.')

def auth():
    path = os.path.join(click.get_app_dir(APP_NAME), 'config.ini')
    config = ConfigParser.RawConfigParser()
    config.read(path)

    try:
        twitter_session = OAuth1Session(\
            config.get(APP_NAME, 'PY_HISS_CONSUMER_KEY'), \
            config.get(APP_NAME, 'PY_HISS_CONSUMER_KEY_SECRET'), \
            config.get(APP_NAME, 'PY_HISS_ACCESS_TOKEN'), \
            config.get(APP_NAME, 'PY_HISS_ACCESS_TOKEN_SECRET'))
    except ConfigParser.NoSectionError:
        click.echo('You need to configure by `hiss setup` command.')
        sys.exit()
    else:
        return twitter_session

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.invoked_subcommand

@cli.command()
def setup():
    """Configure your Twitter auth information.
    """
    configure()

@cli.command()
def reset():
    """Reset your Twitter auth information.
    """
    app_dir = click.get_app_dir(APP_NAME)
    path = os.path.join(app_dir, 'config.ini')
    if os.path.exists(path): os.remove(path)
    click.echo('Configuration has been reset.')

@cli.command()
@click.argument('text')
def say(text):
    """Post given text.
    """
    l = len(text)
    if l > 140:
        click.echo('Tweet length should be <= 140.')
        return

    twitter_session = auth()
    res = twitter_session.post('https://api.twitter.com/1.1/statuses/update.json', params={'status': text})

    if res.status_code == 200: click.echo('Posted.')
    else: click.echo('Faild.')

@cli.command()
@click.option('--count', '-n', default=10, help='Number of tweets.')
def head(count):
    """Display the latest tweets on your timeline like `head` command. (default: 10)
    """
    import json

    twitter_session = auth()
    res = twitter_session.get('https://api.twitter.com/1.1/statuses/home_timeline.json', params={'count': count})

    if res.status_code == 200:
      timeline = json.loads(res.text)
      for tweet in timeline:
          print tweet['text']
    else:
      print 'Error: %d' % res.status_code

