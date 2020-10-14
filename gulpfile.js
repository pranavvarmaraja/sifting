// ======================================================================
// Automate development, build and test processes...
// ======================================================================
//
// Usage:
//          List all possible tasks defined in this gulpfile:
//          $ gulp --tasks
// 
//          Execute a specific task:
//          $ gulp test_svg
//
// Prerequisites:
//          $ pip3 install gulp
// ======================================================================

const { src, dest, watch } = require('gulp');
// Node.js child_process:
// Run Unix commands locally (in a Shell or not):
// Info: https://nodejs.org/api/child_process.html#child_process_child_process_spawn_command_args_options
const { spawn } = require('child_process');


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// Usage: $ gulp test_svg
//
// Description:
//      Automatically runs python -m ./graph_test.py every time this file is saved.
//      Continuously watches for changes, when a change (Save) is detected, it
//      runs in the background as a Unix child process
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function test_svg() {
    watch(
            [
                './svg.py',
                './graph_test.py',
            ],
            {
                events: ['change'],
            },
            function run_svg_script(done) {
                console.log('svg.py changed...');
                run_svg();
                done();
            }
    )
};

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function run_svg(done) {

    const BashRunArgs = [
        '-m',
        'graph_test'
    ]

    const BashCmd = spawn('python', BashRunArgs, { shell: true});

    BashCmd.stdout.on('data', (data) => {
        console.log(`${data}`);
    })

    BashCmd.stderr.on('data', (data) => {
        console.log(`${data}`);
    })

    BashCmd.on('error', function(err) {
        console.log(`child process exited with an error ${err.code}`);
      });      

    BashCmd.on('exit', function(exitCode, exitSignal) {
        // console.log(`child process exited with code ${exitCode} with signal ${exitSignal}`);
      });
    
}
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// Default task :
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function defaultTask(cb) {
    // place code for your default task here
    console.log('For the list of available tasks, type: gulp --tasks');
    cb();
  };
  
  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  // Export functions that can be used publicly :
  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  
  exports.test_svg = test_svg;
  exports.default = defaultTask;
  
  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  