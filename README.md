hiss
===

A simple command-line twitter client.

## Installation

```
$ pip install git+https://github.com/takuti/hiss.git
```

## Usage

### Setup

```
$ hiss setup
```

Enter your Twitter API auth information:

- consumer key
- consumer key secret
- access token
- access token secret

### Tweet

```
$ hiss say [text what you want to tweet]
```

### See the latest tweets on your timeline

show 5 latest tweets:

```
$ hiss head
```

or, you can specify the number of tweets as:

```
$ hiss head -n 10
```

## License

MIT