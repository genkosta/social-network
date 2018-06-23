PIPELINE = {
    'COMPILERS': ('pipeline.compilers.less.LessCompiler',),
    'LESS_BINARY': '/usr/local/bin/lessc',
    'LESS_ARGUMENTS': '--source-map-map-inline',
    'YUGLIFY_BINARY': '/usr/local/bin/yuglify',
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'CLOSURE_BINARY': '/usr/bin/env closure-compiler',
    'CLOSURE_ARGUMENTS': '--language_in=ECMASCRIPT5 --warning_level=QUIET '
                         '--compilation_level WHITESPACE_ONLY --formatting PRINT_INPUT_DELIMITER',
    'JS_COMPRESSOR': 'pipeline.compressors.closure.ClosureCompressor',
    'DISABLE_WRAPPER': True,
    'STYLESHEETS': {
        'all': {
            'source_filenames': (
                'css/custom.css',
            ),
            'output_filename': 'css/all.css',
        },
    },
    'JAVASCRIPT': {
        'all': {
            'source_filenames': (
                'js/custom.js',
            ),
            'output_filename': 'js/all.js',
        }
    }
}
