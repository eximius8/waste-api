from rest_framework import serializers
from .models import WasteComponent

from componentprop.serializers import CategoryPropSerializer, ValuePropSerializer
from litsource.serializers import LitSourceSerializer


class WasteComponentListSerializer(serializers.ModelSerializer):
   

    class Meta:

        model = WasteComponent
        read_only_fields = ('id', 'name', 'other_names')
        fields = ('id', 'name', 'other_names')
        

class WasteComponentSerializer(serializers.ModelSerializer):
   
    #w_value = serializers.ReadOnlyField(source='get_w')
    
    category_props = CategoryPropSerializer(many=True, read_only=True)
    props = ValuePropSerializer(many=True, read_only=True, source='value_props')
    x_value_lit_source = LitSourceSerializer(read_only=True)
    land_concentration_lit_source = LitSourceSerializer(read_only=True)
    
   
    

    def to_representation(self,obj):  
        rep = super(WasteComponentSerializer, self).to_representation(obj)
        rep['props'] += rep['category_props'] 
        rep.pop('category_props')

        if obj.get_s_rastv_pdk_v_score()[0]:
            rep['props'] += [{
                    "name": "lg(S/ПДКв)",
                    "value": obj.get_s_rastv_pdk_v_score()[0],
                    "literature_source": [LitSourceSerializer(obj.s_rastv_lit_source).data,
                                        LitSourceSerializer(obj.pdk_v_lit_source).data],
                    "score": obj.get_s_rastv_pdk_v_score()[1]
                }]
        
        if obj.get_c_nasish_pdk_rz_score()[0]:
            rep['props'] += [{
                    "name": "lg(Cнас/ПДКрз)",
                    "value": obj.get_c_nasish_pdk_rz_score()[0],
                    "literature_source": [LitSourceSerializer(obj.c_nasish_lit_source).data,
                                        LitSourceSerializer(obj.pdk_rz_lit_source).data],
                    "score": obj.get_c_nasish_pdk_rz_score()[1]
                }]
        
        if obj.get_c_nasish_pdk_ss_score()[0]:
            rep['props'] += [{
                    "name": "lg(Cнас/ПДКcc)",
                    "value": obj.get_c_nasish_pdk_ss_score()[0],
                    "literature_source": [LitSourceSerializer(obj.c_nasish_lit_source).data,
                                        LitSourceSerializer(obj.pdk_ss_lit_source).data],
                    "score": obj.get_c_nasish_pdk_ss_score()[1]
                }]

        if obj.get_c_nasish_pdk_mr_score()[0]:
            rep['props'] += [{
                    "name": "lg(Cнас/ПДКмр)",
                    "value": obj.get_c_nasish_pdk_mr_score()[0],
                    "literature_source": [LitSourceSerializer(obj.c_nasish_lit_source).data,
                                        LitSourceSerializer(obj.pdk_mr_lit_source).data],
                    "score": obj.get_c_nasish_pdk_mr_score()[1]
                }]

        if obj.get_BD_score()[0]:
            rep['props'] += [{
                    "name": "БД=БПК5/ХПК 100%",
                    "value": obj.get_BD_score()[0],
                    "literature_source": [LitSourceSerializer(obj.xpk_lit_source).data,
                                        LitSourceSerializer(obj.bpk5_lit_source).data],
                    "score": obj.get_BD_score()[1]
                }]


        for prop, stri in {'pdk_v': "ПДКв, мг/л", 'pdk_ss': "ПДКсс, мг/м3", 'pdk_mr': "ПДКмр, мг/м3"}.items():
            if bool(eval(f'obj.{prop}')):
                rep['props'] += [{
                    "name": stri,
                    "value": eval(f"obj.{prop}"),
                    "literature_source": [LitSourceSerializer(eval(f'obj.{prop}_lit_source')).data],
                    "score": eval(f'obj.get_{prop}_score()')
                }]
        
        return rep  

    class Meta:

        model = WasteComponent        
        fields = ('id', 'name', 'get_x', 'get_z', 'get_log_w', 'get_w', 
        'chemical_type', 'category_props', 'props',  'Binf', 
        'x_value_lit_source', 'land_concentration', 'land_concentration_lit_source')