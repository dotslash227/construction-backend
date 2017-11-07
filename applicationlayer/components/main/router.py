class Router:

    def __init__(self):
        pass

    @staticmethod
    def get_routes():
        return [
            {
                'pattern': '{site}/product',
                'name': 'product'
            },
            {
                'pattern': '{site}/product/mixture',
                'name': 'mixture'
            },
            {
                'pattern': 'site',
                'name': 'site'
            },
            {
                # params ?date=DD/MM/YYYY&chainageId=C1
                'pattern': '{site}/site/{siteId}/chainage',
                'name': 'sand_site_chainage'
            },
            {
                # params ?date=DD/MM/YYYY
                'pattern': '{site}/site/{siteId}/sand',
                'name': 'sand_site'
            },
            {
                'pattern': '{site}/supplier',
                'name': 'supplier'
            },
            {
                'pattern': '{site}/supplier/retrospective',
                'name': 'supplier_retrospective'
            },
            {
                'pattern': '{site}/supplier/{supplier_id}',
                'name': 'supplier_specific'
            },

            {
                'name': 'location',
                'pattern': '{site}/location',
            },
            {
                'name': 'ticket',
                'pattern': '{site}/ticket',
            },
            {
                'pattern': '{site}/ticket/{tickedId}/record_location',
                'name': 'record_location'
            },
            {
                'name': 'gate_pass',
                'pattern': '{site}/gate_pass'
            },
            {
                'name': 'gate_pass_approve',
                'pattern': '{site}/gate_pass/approve'
            },
            {
                'name': 'gate_pass_calculate',
                'pattern': '{site}/gate_pass/calculate'
            },
            {
                'name': 'ticket_print',
                'pattern': '/ticket/{tickedId}/print'
            },
            {
                'name': 'print_receipt',
                'pattern': '/ticket/{tickedId}/receipt'
            },
            {
                'name': 'media',
                'pattern': '/media/{mediaId}'
            },
            {
                'name': 'equipment',
                'pattern': '{site}/equipment'
            },
            {
                'name': 'equipment_logs',
                'pattern': '{site}/equipment/logs',

            },
            {
                'name': 'inventory_check',
                'pattern': '{site}/location/{location_id}/inventory'
            },
            {
                'name': 'materialReceived',
                'pattern': '{site}/{equipment_provider}/materialReceived'
            },
            {
                'name': 'emptyWeight',
                'pattern': '{site}/ticket/{ticket_id}/emptyWeight'
            }



        ]
