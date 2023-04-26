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

Install [Visual Studio Code][vscode]. This repository has configuration for
vscode to make the development experience uniform and smooth for everyone.

[vscode]: https://code.visualstudio.com/

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

To make vscode use the correct Python environment, in a terminal, run...

```sh
pants export ::
```

To activate the virtual environment in a shell, run...

```sh
bash ./dist/export/python/virtualenv/3.8.16/bin/activate
```

### Codegen

Generate Python code using the remote `openapi.json` and [swagger-codegen][swagger-codegen].

[swagger-codegen]: https://github.com/swagger-api/swagger-codegen

#### Installation

```sh
brew install swagger-codegen
```

#### Adding a Client

1. Add a dir under `openapi`
2. Put the API's `openapi.json` in that directory
3. Run `./scripts/codegen.sh`

#### Getting Help

To see additional options:

```sh
swagger-codegen generate --help
swagger-codegen config-help -l python
```

### Running Tests

To test everything, run...

```sh
pants test ::
```

To test a single file, run...

```sh
pants test --no-use-coverage ${file}
```

### Auto Format Code

To format everything and fix the code for Flake8, run...

```sh
pants fmt ::
pants fix ::
```

### Local Testing via REPL

To get a Python shell to test code, [comment out the `python_distribution` target][pants-16985] in `/BUILD`. Then run...

```sh
pants repl ::
```

[pants-16985]: https://github.com/pantsbuild/pants/issues/16985

### Viewing Docs

To view docs generated from the `docs` folder, run...

```sh
./scripts/slate.sh serve
```

Then, in a browser, open http://localhost:8000.

### Building Docs Locally

To build docs locally, run...

```sh
./scripts/slate.sh build
```

## Deployments and Releases

### Developer Documentation

The slate documentation deploys on every `master` branch merge.

### Release Process

1. Create a tagged release with an appropriate semantic version eg. if the current version is 0.4.2, the next patch version would be 0.4.3, or a next minor version would be 0.5.0. Use the [New Release Form][new-release-form] to create the release. Make sure it is marked as **pre-release**.
1. Install the SDK from TestPyPI: `pip install --upgrade --index-url https://test.pypi.org/simple/ frontrunner-sdk`.
1. Edit the release -- remove the checkmark from "Set as a pre-release" and save.
1. Install the SDK from PyPI (production): `pip install --upgrade frontrunner-sdk`

[new-release-form]: https://github.com/GetFrontrunner/frontrunner-sdk/releases/new

Test PyPI: https://test.pypi.org/project/frontrunner-sdk/
Prod PyPI: https://pypi.org/project/frontrunner-sdk/
