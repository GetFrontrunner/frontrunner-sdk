# Frontrunner SDK

[Frontrunner][frontrunner] is the first zero gas fee, decentralized sports
prediction market built on blockchain where you get the best odds with no house
edge.

[frontrunner]: https://www.getfrontrunner.com/

This is an SDK which allows you to interact with our public-facing API easily
via Python.

## Developer

Note: this assumes OSX

### Prerequisite Installation

Install [`brew`][brew]. This will be used to install other required tooling.

[brew]: https://brew.sh/

Install [Visual Studio Code]. This repository has configuration for vscode to
make the development experience uniform and smooth for everyone.

```sh
brew install --cask visual-studio-code
```

Install [`pants`][pants]. Pants is a generic build tool that supports multiple
languages and tools. Both local builds and CI builds use Pants.

[pants]: https://www.pantsbuild.org/docs/welcome-to-pants

```sh
brew install pantsbuild/tap/pants
```

Clone the repository. Then, open up the repository in vscode.
[Install the recommended extensions][install-recommended-extensions] for this
workspace. Restart vscode.

[install-recommended-extensions]: https://code.visualstudio.com/docs/editor/extension-marketplace#_workspace-recommended-extensions

In a terminal at the root of the repository, test your setup by running...

```sh
pants lint ::
pants check ::
pants test ::
```

### Running Tests

To test everything, run...

```sh
pants test ::
```

To test a single file, run...

```sh
pants test ${file}
```

### Local Testing via REPL

To get a Python shell to test code, run...

```sh
pants repl ::
```
