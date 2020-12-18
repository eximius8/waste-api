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
   
    w_value = serializers.ReadOnlyField(source='get_w')
    
    category_props = CategoryPropSerializer(many=True, read_only=True)
    value_props = ValuePropSerializer(many=True, read_only=True)

    def to_representation(self,obj):  
        rep = super(WasteComponentSerializer, self).to_representation(obj)

        if obj.get_s_rastv_pdk_v_score()[0]:
            rep['value_props'] += [{
                    "value_type": "lg(S/ПДКв)",
                    "prop_float_value": obj.get_s_rastv_pdk_v_score()[0],
                    "literature_source": [LitSourceSerializer(obj.s_rastv_lit_source).data,
                                        LitSourceSerializer(obj.pdk_v_lit_source).data],
                    "get_score": obj.get_s_rastv_pdk_v_score()[1]
                }]
        
        if obj.get_c_nasish_pdk_rz_score()[0]:
            rep['value_props'] += [{
                    "value_type": "lg(Cнас/ПДКрз)",
                    "prop_float_value": obj.get_c_nasish_pdk_rz_score()[0],
                    "literature_source": [LitSourceSerializer(obj.c_nasish_lit_source).data,
                                        LitSourceSerializer(obj.pdk_rz_lit_source).data],
                    "get_score": obj.get_c_nasish_pdk_rz_score()[1]
                }]
        
        if obj.get_c_nasish_pdk_ss_score()[0]:
            rep['value_props'] += [{
                    "value_type": "lg(Cнас/ПДКcc)",
                    "prop_float_value": obj.get_c_nasish_pdk_ss_score()[0],
                    "literature_source": [LitSourceSerializer(obj.c_nasish_lit_source).data,
                                        LitSourceSerializer(obj.pdk_ss_lit_source).data],
                    "get_score": obj.get_c_nasish_pdk_ss_score()[1]
                }]

        if obj.get_c_nasish_pdk_mr_score()[0]:
            rep['value_props'] += [{
                    "value_type": "lg(Cнас/ПДКмр)",
                    "prop_float_value": obj.get_c_nasish_pdk_mr_score()[0],
                    "literature_source": [LitSourceSerializer(obj.c_nasish_lit_source).data,
                                        LitSourceSerializer(obj.pdk_mr_lit_source).data],
                    "get_score": obj.get_c_nasish_pdk_mr_score()[1]
                }]

        if obj.get_BD_score()[0]:
            rep['value_props'] += [{
                    "value_type": "БД=БПК5/ХПК 100%",
                    "prop_float_value": obj.get_BD_score()[0],
                    "literature_source": [LitSourceSerializer(obj.xpk_lit_source).data,
                                        LitSourceSerializer(obj.bpk5_lit_source).data],
                    "get_score": obj.get_BD_score()[1]
                }]


        for prop, stri in {'pdk_v': "ПДКв, мг/л", 'pdk_ss': "ПДКсс, мг/м3", 'pdk_mr': "ПДКмр, мг/м3"}.items():
            if bool(eval(f'obj.{prop}')):
                rep['value_props'] += [{
                    "value_type": stri,
                    "prop_float_value": eval(f"obj.{prop}"),
                    "literature_source": [LitSourceSerializer(eval(f'obj.{prop}_lit_source')).data],
                    "get_score": eval(f'obj.get_{prop}_score()')
                }]
        
        return rep  

    class Meta:

        model = WasteComponent        
        fields = ('id', 'name', 'w_value', 'chemical_type', 'category_props', 'value_props',  'Binf')