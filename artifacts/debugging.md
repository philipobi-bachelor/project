# VS Code debugging configuration for basf2

I used the following debug config in `.vscode/launch.json` (replace program args and paths as needed):
```json
{
  "version":"0.2.0",
  "configurations":[
    {
      "name":"GDB basf2",
      "type":"cppdbg",
      "cwd":"${workspaceFolder}",
      "request":"launch",
      "program":"${workspaceFolder}/bin/Linux_x86_64/debug/basf2",
      "args":[
        "ARGS_FOR_BASF2"
      ],
      "stopAtEntry":true,
      "MIMode":"gdb",
      "miDebuggerPath":"/PATH/TO/bin/gdb",
      "envFile":"${workspaceFolder}/.env",
      "setupCommands":[
        {
          "description":"Enable pretty-printing for gdb",
          "text":"python import sys; sys.path.append('/PATH/TO/gcc-14.1.0/python');sys.path.insert(0, '/usr/bin/python');from libstdcxx.v6.printers import register_libstdcxx_printers;register_libstdcxx_printers(None)",
          "ignoreFailures":false
        },
        {
          "description":"Enable pretty-printing for gdb",
          "text":"-enable-pretty-printing",
          "ignoreFailures":true
        }
      ]
    }
  ]
}
```
More information on the C++ STL pretty printers for GDB: https://sourceware.org/gdb/wiki/STLSupport

Basf2 requires specific environment values to run; which are exactly needed I do not know, therefore I simply dumped my entire shell environment to `.env` after running `b2setup` and `b2code-option debug` using:
```sh
printenv | awk -F= '{print $1"=\"" $2 "\"" }' > .env
```

Directory structure:
```
.
├── .env
├── .vscode
...
├── alignment
├── analysis
├── arich
├── b2bii
...
├── trg
├── validation
├── vxd
└── whatsnew.rst
```