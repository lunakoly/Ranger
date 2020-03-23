# Overview
This utility can split one single video into a bunch of other videos each one being a sequence of subclips of the original video. Text clips with captions/comments are also supported.

Source video splitting is described via so called _ranges-files_. You can also download VS Code extension for _ranges-files_ syntax highlighting [here](https://github.com/lunakoly/RangesFileLanguage).

See _test_counter_ if you need an example.

# Usage
The main executable is _python/cut.py_.
```bash
$ cut [options...]
```
Options can be specified as `-c <...> -i <...> -r <...> -o <...>` or `-ciro <...> <...> <...> <...>`. Full name is available for each option as well.

# Options
- `-i`, `--input <file>` - Specify the input video file. Make sure it has no issues with _tbr_ (can be fixed via `ffmpeg -hide_banner -i <input video> -c copy <fixed video>`). The default value is _input.mp4_.

- `-r`, `--ranges <file>` - Specify the ranges file. The default value is _ranges.rng_.

- `-o`, `--output <pattern>` - Specify the output files pattern. Use `{}` to substitute the marker name. The default value is _output\_{}.mp4_.

- `-c`, `--collect <marker>` - Specify the marker that should collect all other subclips into itself. Knowing that marker `main` is used as the default marker for all unmarked clips, you can use `--collect main` to collect all the clips together into the `main` sequence.

- `-f`, `--fontsize <size>` - Specify the size of the font (in _px_) to use for text clips. By default font is selected adaptevely to suit any resolution. There's no way to set adaptive font size coefficient manually right now.

- `-u`, `--inclusive` - If specified, stop time value of every video clip range in incremented by one second.

- `-h`, `--help` - Show help message.

# Ranges-files
VS Code syntax highlighting extension is available [here](https://github.com/lunakoly/RangesFileLanguage).

Ranges files follow the following syntax rules:
- Empty lines are ignored.
- Lines that match the pattern `<time>-<time> [marker]` are treated as _time directives_ and define a subclip of the source video.
- Lines that don't match _time directives_ pattern are treated as text clips (duration = 5sec) and get collected by the parser until a video clip is met. When it happens, text clips are treated as comments to the following video clip and inserted right before it.

`time` is a value that looks like: `h:m:s` (e.g. `1:12:56.324`). Other formats are: `m:s` and `s`.

`marker` is an identifier matched via python `\w+` (may contain digits, letters and `_`).