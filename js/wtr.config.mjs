import {importMapsPlugin} from '@web/dev-server-import-maps';
import {playwrightLauncher} from '@web/test-runner-playwright';

export const importMap = {
    imports: {
        'jquery': './node_modules/jquery/dist-module/jquery.module.js'
    },
};

export default {
    nodeResolve: true,
    browsers: [
        playwrightLauncher({product: 'chromium'}),
    ],
    testFramework: {
        path: './node_modules/web-test-runner-qunit/dist/autorun.js',
        config: {
            noglobals: false
        }
    },
    files: [
        'js/tests/**/test_*.js'
    ],
    coverageConfig: {
        include: ['**/js/src/**/*.js'],
        exclude: ['**/node_modules/**', 'sources/**']
    },
    plugins: [
        importMapsPlugin({
            inject: {importMap},
        }),
    ],
}
