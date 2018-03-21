import { FuseNavigationModelInterface } from '../core/components/navigation/navigation.model';

export class FuseNavigationModel implements FuseNavigationModelInterface
{
    public model: any[];

    constructor()
    {
        this.model = [
            {
                'id'      : 'applications',
                'title'   : 'Applications',
                'translate': 'NAV.APPLICATIONS',
                'type'    : 'group',
                'children': [
                    {
                        'id'   : 'compare',
                        'title': 'Compare',
                        'translate': 'NAV.COMPARE.TITLE',
                        'type' : 'item',
                        'icon' : 'email',
                        'url'  : '/compare',
                        // 'badge': {
                        //     'title': 25,
                        //     'translate': 'NAV.COMPARE.BADGE',
                        //     'bg'   : '#F44336',
                        //     'fg'   : '#FFFFFF'
                        // }
                    },
                    {
                        'id'   : 'upload',
                        'title': 'Upload',
                        'translate': 'NAV.UPLOAD.TITLE',
                        'type' : 'item',
                        'icon' : 'email',
                        'url'  : '/upload',
                        // 'badge': {
                        //     'title': 25,
                        //     'translate': 'NAV.UPLOAD.BADGE',
                        //     'bg'   : '#F44336',
                        //     'fg'   : '#FFFFFF'
                        // }
                    },
                    
                ]
            }
        ];
    }
}
