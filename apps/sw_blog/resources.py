from import_export.resources import ModelResource 
from .models import * 


from box.core.sw_global_config.models import GlobalMarker 


class PostResource(ModelResource):
    class Meta:
        model = Post 
        exclude = [
            'created',
            'updated',
            'code',
            'order',
            'slug',
        ]

    def before_import_row(self, row, **kwargs):
        self.handle_markers_import(row)

    def handle_markers_import(self, row):
        if row.get('markers'):
            markers = []
            marker_names = row['markers'].split(',')
            if not marker_names:
                marker_names =  list(row['markers'])
            for marker_name in marker_names:
                # for marker in GlobalMarker.objects.all():
                    
                #     print('marker.name', marker.name.strip().lower())
                #     print('marker_name', marker_name.strip().lower())
                #     print( marker.name.strip().lower() == marker_name.strip().lower())

                marker = GlobalMarker.objects.get(
                # marker, _ = GlobalMarker.objects.get_or_create(
                    # name__iexact=marker_name.strip().lower()
                    name=marker_name.strip().lower()
                )
                markers.append(str(marker.id))
            row['markers'] = ','.join(markers)

    def dehydrate_markers(self, post):
        markers = None 
        if post.id and post.markers.all().exists():
            markers = ','.join([marker.name.lower().strip() for marker in post.markers.all()])
        return markers

