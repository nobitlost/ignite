Search.setIndex({docnames:["examples","index","modules","readme","source/modules","source/pyignite","source/pyignite.api","source/pyignite.connection","source/pyignite.datatypes","source/pyignite.queries"],envversion:53,filenames:["examples.rst","index.rst","modules.rst","readme.rst","source/modules.rst","source/pyignite.rst","source/pyignite.api.rst","source/pyignite.connection.rst","source/pyignite.datatypes.rst","source/pyignite.queries.rst"],objects:{"":{pyignite:[5,0,0,"-"]},"pyignite.api":{cache_config:[6,0,0,"-"],key_value:[6,0,0,"-"],result:[6,0,0,"-"],sql:[6,0,0,"-"]},"pyignite.api.cache_config":{cache_create:[6,1,1,""],cache_destroy:[6,1,1,""],cache_get_configuration:[6,1,1,""],cache_get_names:[6,1,1,""],cache_get_or_create:[6,1,1,""]},"pyignite.api.key_value":{cache_clear:[6,1,1,""],cache_clear_key:[6,1,1,""],cache_clear_keys:[6,1,1,""],cache_contains_key:[6,1,1,""],cache_contains_keys:[6,1,1,""],cache_get:[6,1,1,""],cache_get_all:[6,1,1,""],cache_get_and_put:[6,1,1,""],cache_get_and_put_if_absent:[6,1,1,""],cache_get_and_remove:[6,1,1,""],cache_get_and_replace:[6,1,1,""],cache_get_size:[6,1,1,""],cache_put:[6,1,1,""],cache_put_all:[6,1,1,""],cache_put_if_absent:[6,1,1,""],cache_remove_all:[6,1,1,""],cache_remove_if_equals:[6,1,1,""],cache_remove_key:[6,1,1,""],cache_remove_keys:[6,1,1,""],cache_replace:[6,1,1,""],cache_replace_if_equals:[6,1,1,""]},"pyignite.api.result":{APIResult:[6,2,1,""],hashcode:[6,1,1,""]},"pyignite.connection":{Connection:[7,2,1,""],PrefetchConnection:[7,2,1,""],SocketError:[7,5,1,""],handshake:[7,0,0,"-"]},"pyignite.connection.Connection":{close:[7,3,1,""],connect:[7,3,1,""],read_response:[7,3,1,""],recv:[7,3,1,""],send:[7,3,1,""],socket:[7,4,1,""]},"pyignite.connection.PrefetchConnection":{conn:[7,4,1,""],prefetch:[7,4,1,""],recv:[7,3,1,""]},"pyignite.connection.handshake":{HandshakeRequest:[7,2,1,""],read_response:[7,1,1,""]},"pyignite.connection.handshake.HandshakeRequest":{client_code:[7,4,1,""],length:[7,4,1,""],op_code:[7,4,1,""],version_major:[7,4,1,""],version_minor:[7,4,1,""],version_patch:[7,4,1,""]},"pyignite.datatypes":{cache_config:[8,0,0,"-"],complex:[8,0,0,"-"],key_value:[8,0,0,"-"],null_object:[8,0,0,"-"],primitive:[8,0,0,"-"],primitive_arrays:[8,0,0,"-"],primitive_objects:[8,0,0,"-"],standard:[8,0,0,"-"],type_codes:[8,0,0,"-"]},"pyignite.datatypes.cache_config":{CacheMode:[8,2,1,""],IndexType:[8,2,1,""],PartitionLossPolicy:[8,2,1,""],RebalanceMode:[8,2,1,""],Struct:[8,2,1,""],StructArray:[8,2,1,""],WriteSynchronizationMode:[8,2,1,""]},"pyignite.datatypes.cache_config.CacheMode":{LOCAL:[8,4,1,""],PARTITIONED:[8,4,1,""],REPLICATED:[8,4,1,""]},"pyignite.datatypes.cache_config.IndexType":{FULLTEXT:[8,4,1,""],GEOSPATIAL:[8,4,1,""],SORTED:[8,4,1,""]},"pyignite.datatypes.cache_config.PartitionLossPolicy":{IGNORE:[8,4,1,""],READ_ONLY_ALL:[8,4,1,""],READ_ONLY_SAFE:[8,4,1,""],READ_WRITE_ALL:[8,4,1,""],READ_WRITE_SAFE:[8,4,1,""]},"pyignite.datatypes.cache_config.RebalanceMode":{ASYNC:[8,4,1,""],NONE:[8,4,1,""],SYNC:[8,4,1,""]},"pyignite.datatypes.cache_config.Struct":{parse:[8,3,1,""],to_python:[8,3,1,""]},"pyignite.datatypes.cache_config.StructArray":{parse:[8,3,1,""],to_python:[8,3,1,""]},"pyignite.datatypes.cache_config.WriteSynchronizationMode":{FULL_ASYNC:[8,4,1,""],FULL_SYNC:[8,4,1,""],PRIMARY_SYNC:[8,4,1,""]},"pyignite.datatypes.complex":{AnyDataObject:[8,2,1,""],CollectionObject:[8,2,1,""],MapObject:[8,2,1,""],ObjectArrayObject:[8,2,1,""]},"pyignite.datatypes.complex.AnyDataObject":{from_python:[8,6,1,""],get_subtype:[8,7,1,""],parse:[8,6,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.complex.CollectionObject":{build_header:[8,6,1,""],tc_type:[8,4,1,""],type_or_id_name:[8,4,1,""]},"pyignite.datatypes.complex.MapObject":{HASH_MAP:[8,4,1,""],LINKED_HASH_MAP:[8,4,1,""],build_header:[8,6,1,""],from_python:[8,6,1,""],parse:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.complex.ObjectArrayObject":{build_header:[8,6,1,""],from_python:[8,6,1,""],parse:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""],type_or_id_name:[8,4,1,""]},"pyignite.datatypes.key_value":{PeekModes:[8,2,1,""]},"pyignite.datatypes.key_value.PeekModes":{ALL:[8,4,1,""],BACKUP:[8,4,1,""],NEAR:[8,4,1,""],PRIMARY:[8,4,1,""]},"pyignite.datatypes.null_object":{Null:[8,2,1,""]},"pyignite.datatypes.null_object.Null":{build_c_type:[8,6,1,""],from_python:[8,7,1,""],parse:[8,6,1,""],to_python:[8,7,1,""]},"pyignite.datatypes.primitive":{Bool:[8,2,1,""],Byte:[8,2,1,""],Char:[8,2,1,""],Double:[8,2,1,""],Float:[8,2,1,""],Int:[8,2,1,""],Long:[8,2,1,""],Primitive:[8,2,1,""],Short:[8,2,1,""]},"pyignite.datatypes.primitive.Bool":{c_type:[8,4,1,""]},"pyignite.datatypes.primitive.Byte":{c_type:[8,4,1,""]},"pyignite.datatypes.primitive.Char":{c_type:[8,4,1,""],from_python:[8,6,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.primitive.Double":{c_type:[8,4,1,""]},"pyignite.datatypes.primitive.Float":{c_type:[8,4,1,""]},"pyignite.datatypes.primitive.Int":{c_type:[8,4,1,""]},"pyignite.datatypes.primitive.Long":{c_type:[8,4,1,""]},"pyignite.datatypes.primitive.Primitive":{c_type:[8,4,1,""],from_python:[8,6,1,""],parse:[8,6,1,""],to_python:[8,7,1,""]},"pyignite.datatypes.primitive.Short":{c_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays":{BoolArray:[8,2,1,""],BoolArrayObject:[8,2,1,""],ByteArray:[8,2,1,""],ByteArrayObject:[8,2,1,""],CharArray:[8,2,1,""],CharArrayObject:[8,2,1,""],DoubleArray:[8,2,1,""],DoubleArrayObject:[8,2,1,""],FloatArray:[8,2,1,""],FloatArrayObject:[8,2,1,""],IntArray:[8,2,1,""],IntArrayObject:[8,2,1,""],LongArray:[8,2,1,""],LongArrayObject:[8,2,1,""],ShortArray:[8,2,1,""],ShortArrayObject:[8,2,1,""]},"pyignite.datatypes.primitive_arrays.BoolArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.BoolArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.ByteArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.ByteArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.CharArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.CharArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.primitive_arrays.DoubleArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.DoubleArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.FloatArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.FloatArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.IntArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.IntArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.LongArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.LongArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.ShortArray":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_arrays.ShortArrayObject":{c_type:[8,4,1,""],primitive_type:[8,4,1,""]},"pyignite.datatypes.primitive_objects":{BoolObject:[8,2,1,""],ByteObject:[8,2,1,""],CharObject:[8,2,1,""],DataObject:[8,2,1,""],DoubleObject:[8,2,1,""],FloatObject:[8,2,1,""],IntObject:[8,2,1,""],LongObject:[8,2,1,""],ShortObject:[8,2,1,""]},"pyignite.datatypes.primitive_objects.BoolObject":{c_type:[8,4,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.ByteObject":{c_type:[8,4,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.CharObject":{c_type:[8,4,1,""],from_python:[8,6,1,""],to_python:[8,6,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.DataObject":{build_c_type:[8,6,1,""],c_type:[8,4,1,""],from_python:[8,6,1,""],parse:[8,6,1,""],to_python:[8,7,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.DoubleObject":{c_type:[8,4,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.FloatObject":{c_type:[8,4,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.IntObject":{c_type:[8,4,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.LongObject":{c_type:[8,4,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.primitive_objects.ShortObject":{c_type:[8,4,1,""],type_code:[8,4,1,""]},"pyignite.datatypes.standard":{BinaryEnumArrayObject:[8,2,1,""],BinaryEnumObject:[8,2,1,""],DateArray:[8,2,1,""],DateArrayObject:[8,2,1,""],DateObject:[8,2,1,""],DecimalArray:[8,2,1,""],DecimalArrayObject:[8,2,1,""],DecimalObject:[8,2,1,""],EnumArray:[8,2,1,""],EnumArrayObject:[8,2,1,""],EnumObject:[8,2,1,""],ObjectArray:[8,2,1,""],String:[8,2,1,""],StringArray:[8,2,1,""],StringArrayObject:[8,2,1,""],TimeArray:[8,2,1,""],TimeArrayObject:[8,2,1,""],TimeObject:[8,2,1,""],TimestampArray:[8,2,1,""],TimestampArrayObject:[8,2,1,""],TimestampObject:[8,2,1,""],UUIDArray:[8,2,1,""],UUIDArrayObject:[8,2,1,""],UUIDObject:[8,2,1,""]},"pyignite.datatypes.standard.BinaryEnumArrayObject":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.BinaryEnumObject":{tc_type:[8,4,1,""]},"pyignite.datatypes.standard.DateArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.DateArrayObject":{standard_type:[8,4,1,""],tc_type:[8,4,1,""]},"pyignite.datatypes.standard.DateObject":{build_c_type:[8,6,1,""],from_python:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.standard.DecimalArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.DecimalArrayObject":{standard_type:[8,4,1,""],tc_type:[8,4,1,""]},"pyignite.datatypes.standard.DecimalObject":{build_c_header:[8,6,1,""],from_python:[8,6,1,""],parse:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.standard.EnumArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.EnumArrayObject":{build_header_class:[8,6,1,""],from_python:[8,6,1,""],standard_type:[8,4,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.standard.EnumObject":{build_c_type:[8,6,1,""],from_python:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.standard.ObjectArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.String":{build_c_type:[8,6,1,""],from_python:[8,6,1,""],parse:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,7,1,""]},"pyignite.datatypes.standard.StringArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.StringArrayObject":{standard_type:[8,4,1,""],tc_type:[8,4,1,""]},"pyignite.datatypes.standard.TimeArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.TimeArrayObject":{standard_type:[8,4,1,""],tc_type:[8,4,1,""]},"pyignite.datatypes.standard.TimeObject":{build_c_type:[8,6,1,""],from_python:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.standard.TimestampArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.TimestampArrayObject":{standard_type:[8,4,1,""],tc_type:[8,4,1,""]},"pyignite.datatypes.standard.TimestampObject":{build_c_type:[8,6,1,""],from_python:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.datatypes.standard.UUIDArray":{standard_type:[8,4,1,""]},"pyignite.datatypes.standard.UUIDArrayObject":{standard_type:[8,4,1,""],tc_type:[8,4,1,""]},"pyignite.datatypes.standard.UUIDObject":{build_c_type:[8,6,1,""],from_python:[8,6,1,""],tc_type:[8,4,1,""],to_python:[8,6,1,""]},"pyignite.queries":{Query:[9,2,1,""],Response:[9,2,1,""],op_codes:[9,0,0,"-"]},"pyignite.queries.Query":{build_c_type:[9,6,1,""],from_python:[9,3,1,""],op_code:[9,4,1,""]},"pyignite.queries.Response":{build_header:[9,7,1,""],parse:[9,3,1,""],to_python:[9,3,1,""]},"pyignite.utils":{is_hinted:[5,1,1,""],is_iterable:[5,1,1,""]},pyignite:{api:[6,0,0,"-"],connection:[7,0,0,"-"],constants:[5,0,0,"-"],datatypes:[8,0,0,"-"],queries:[9,0,0,"-"],utils:[5,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","method","Python method"],"4":["py","attribute","Python attribute"],"5":["py","exception","Python exception"],"6":["py","classmethod","Python class method"],"7":["py","staticmethod","Python static method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:method","4":"py:attribute","5":"py:exception","6":"py:classmethod","7":"py:staticmethod"},terms:{"0x01":2,"0x02":2,"0x03":2,"0x04":2,"0x05":2,"0x06":2,"0x07":2,"0x08":2,"0x09":2,"0x0a":2,"0x0b":2,"0x0c":2,"0x0d":2,"0x0e":2,"0x0f":2,"0x10":2,"0x11":2,"0x12":2,"0x13":2,"0x14":2,"0x15":2,"0x16":2,"0x17":2,"0x18":2,"0x19":2,"0x1b":2,"0x1c":2,"0x1d":2,"0x1e":2,"0x1f":2,"0x21":2,"0x22":2,"0x23":2,"0x24":2,"0x65":2,"0x67":2,"10m":8,"boolean":6,"byte":[0,2,7,8],"case":[2,6,8],"char":[2,8],"class":[2,6,7,8,9],"default":[0,3,6],"enum":[2,8],"float":[2,8],"function":[2,6,8],"import":[0,2],"int":[2,6,8,9],"long":[2,8],"new":6,"null":[2,6,8],"return":[2,6],"short":[2,8],"static":[8,9],"true":[0,6],And:3,For:[2,8],Its:8,NEAR:[6,8],Not:[0,2,8],The:[2,6,8],Then:3,There:8,These:[2,6,9],_build:3,_ctype:7,abbrevi:3,abil:3,about:9,access:6,accuraci:8,activ:3,actual:[2,6,8],addopt:3,aka:8,alia:8,alien:2,all:[2,3,6,8],allow:2,allow_non:8,along:[2,8],alreadi:6,also:[2,8],ambigu:2,analyt:3,ani:[6,8],annoi:8,anoth:[0,8],any_object:[],anydataobject:[2,8],apach:[2,3,6],api:[0,4,5],apidoc:3,apiresult:[2,6],appli:6,applic:3,arg:8,arrai:[2,8],arrayobject:2,associ:6,async:8,attr:3,backup:[6,8],backups_numb:0,base:[2,6,7,8,9],basic:[1,9],bear:8,becaus:8,between:6,binari:[2,3,6,8,9],binaryenumarrayobject:8,binaryenumobject:[2,8],blob:2,bool:[2,6,8],boolarrai:8,boolarrayobject:[2,8],boolobject:[2,8],both:[0,6],bottom:2,bring:2,broad:8,brought:3,browser:3,bucket:6,buffers:7,build:3,build_c_head:8,build_c_typ:[8,9],build_head:[8,9],build_header_class:8,built:8,bytearrai:8,bytearrayobject:[2,8],byteobject:[2,8],c_bool:8,c_byte:8,c_doubl:8,c_float:8,c_int:8,c_long:8,c_short:8,c_type:8,cach:[1,2,3,6],cache_clear:6,cache_clear_kei:6,cache_config:[2,4,5],cache_contains_kei:6,cache_cr:[0,6],cache_destroi:[0,6],cache_get:[0,6],cache_get_al:6,cache_get_and_put:6,cache_get_and_put_if_abs:6,cache_get_and_remov:6,cache_get_and_replac:6,cache_get_configur:[0,6],cache_get_nam:[0,6],cache_get_or_cr:6,cache_get_s:6,cache_key_configur:0,cache_mod:0,cache_nam:0,cache_put:[0,6],cache_put_al:6,cache_put_if_abs:6,cache_remove_al:6,cache_remove_if_equ:6,cache_remove_kei:[0,6],cache_replac:6,cache_replace_if_equ:6,cachemod:8,calcul:[6,8],call:6,can:[2,3,6,8],centric:3,certain:2,charact:[2,8],chararrai:8,chararrayobject:[2,8],charobject:[0,2,8],check:5,checkout:3,choic:6,choos:2,classmethod:[8,9],clean:3,cleanup:1,clear:6,client:[2,3,6],client_cod:7,clone:3,close:[0,7],cluster:[3,6],code:[2,6,8,9],collect:[2,8],collectionobject:[2,8],com:3,combin:3,command:3,common:8,commun:[3,6],compar:6,complex:[2,4,5],conceptu:2,configur:[1,2,6],conn:[0,6,7,8,9],connect:[1,3,4,5,6,8,9],consist:2,constant:[4,9],construct:2,constructor:2,contain:[5,6,8,9],content:[1,2],control:6,convers:[2,8],convert:6,copy_on_read:0,correspond:8,count:[6,8],counter:8,counter_typ:8,cov:3,cover:8,coverag:3,creat:[1,3,6,8],ctype:8,ctype_object:[8,9],ctypes_object:8,current:6,dai:8,data:[2,5,6,7,8],data_region_nam:0,databas:3,dataclass:6,dataobject:8,datatyp:[0,1,4,5],date:2,datearrai:8,datearrayobject:[2,8],dateobject:[2,8],datetim:[2,8],decim:[2,8],decimalarrai:8,decimalarrayobject:[2,8],decimalobject:[2,8],decod:8,default_lock_timeout:0,defin:2,definit:2,delet:0,deliv:3,delta:8,depend:3,descript:[2,6],deseri:[2,8],design:6,destroi:[0,6],detail:2,detect:7,develop:3,dict:[2,6,8,9],dictionari:[6,8],differ:[6,8],distribut:3,distutil:3,divid:2,doc:[2,3,7],document:6,doe:[3,6],doubl:[2,8],doublearrai:8,doublearrayobject:[2,8],doubleobject:[2,8],due:6,dynam:2,each:[2,3,6],eager_ttl:0,edit:1,either:6,encod:8,end:2,endian:8,entiti:6,entri:6,enumarrai:8,enumarrayobject:[2,8],enumer:8,enumobject:[2,8],environ:3,epoch:8,equal:6,error:[2,6,7],even:2,everi:2,exactli:8,exampl:[1,3],except:7,exist:[0,3,6],extens:2,failur:6,fals:[0,6,8],feel:3,field:[2,6,8],find:2,fix:2,flag:[6,7],fledg:3,floatarrai:8,floatarrayobject:[2,8],floatobject:[2,8],flow:2,follow:[2,8,9],form:6,fraction:8,fragment:7,free:3,from:[1,2,3,6,8],from_python:[8,9],full:3,full_async:8,full_sync:8,fulltext:8,gener:[6,8],geospati:8,get:[1,6],get_subtyp:8,git:3,github:3,give:2,given:[3,6],global:8,gone:6,good:8,gori:2,group_nam:0,guess:2,guesswork:8,guid:8,had:6,handl:[2,6],handshak:[2,4,5,6],handshakerequest:7,has:[2,6],hash:6,hash_cod:[0,6],hash_map:8,hashcod:[0,6],hassl:8,have:[2,8],header:8,hint:[1,2,5,6,8],histor:6,hold:8,hood:2,host:[2,3,6,7],howev:2,howto:7,hpet:8,html:[3,7],http:7,identifi:[6,8],ignit:[2,3,6,8,9],ignor:8,implement:[0,2,6],importantli:9,includ:8,independ:8,index:[1,3],indextyp:8,indic:6,indigen:2,inform:[1,9],initi:6,inspect:[1,2],instal:1,instanc:[2,8],instanti:[2,6],instead:[2,8],intarrai:8,intarrayobject:[2,8],integ:[2,8],integr:3,interact:2,intern:[5,8],interoper:[2,8],intobject:[2,8],invalid:0,is_hint:5,is_iter:5,is_onheap_cache_en:0,item:[5,6],iter:[2,5,8],its:[2,5,6,8],itself:8,jan:8,just:[2,8],keep:[6,8],kei:[1,2,6,8],key_hint:[0,6],key_valu:[2,4,5],kill:8,languag:8,length:[0,7,8],less:8,let:[0,6],librari:[2,3],licens:1,lifecycl:6,lightweight:3,like:[6,8],limit:6,line:[2,3],link:2,linked_hash_map:8,list:[1,2,6,8,9],listen:6,littl:8,local:8,localhost:3,logic:2,longarrai:8,longarrayobject:[2,8],longobject:[0,2,8],made:[6,8],mai:[2,3,6,8],make:3,manag:2,manipul:[2,6],map:[2,6,8],mapobject:[2,8],max_query_iter:0,mean:[2,6],measur:3,member:7,memcach:[2,6],memori:[0,3],messag:[0,2,6],metaclass:8,midnight:8,millisecond:8,mind:8,minimum:8,mismatch:2,modul:[1,3,4],more:2,most:[2,9],multipl:[3,6],naiv:8,name:[0,2,6,9],nanosecond:8,nativ:2,natur:2,need:2,negoti:2,nest:8,network:7,nice:2,nobitlost:3,node:[3,6],non:[0,6],none:[0,2,6,7,8,9],nonetyp:2,note:2,noth:6,notifi:6,notion:2,now:0,null_object:[4,5],number:[2,6,8],object:[2,6,7,8,9],objectarrai:8,objectarrayobject:[2,8],oblig:2,obtain:6,old:[3,6],omit:6,omnipot:2,omnivor:2,onc:0,one:[2,8,9],onli:[0,6,8],onto:6,op_cod:[4,5,7],open:[1,3],oper:[2,9],option:[3,6],ordereddict:[0,2,6,8],ordinari:8,org:7,other:[2,3,6],otherwis:6,overli:2,overrid:3,overwrit:6,packag:4,page:1,pair:[6,8],paramet:[3,6],pars:[2,8,9],parser:2,part:[2,6],particular:6,partit:[6,8],partition_loss_polici:0,partitionlosspolici:8,pascal:8,pass:[2,6],past:8,payload:[2,8],peek_mod:6,peekmod:[6,8],persist:6,perspect:8,petabyt:3,pick:2,pip:3,platform:3,plu:8,port:[2,3,6,7],power:2,prefetch:7,prefetchconnect:7,prepend:[2,8],prerequisit:1,present:6,previou:6,primari:[6,8],primary_sync:8,primit:[2,4,5],primitive_arrai:[4,5],primitive_object:[4,5],primitive_typ:8,primitivearrai:8,primitivearrayobject:8,print:0,process:[2,3],project:3,proper:6,protocol:[2,3,6,9],provid:[3,6],put:[1,6],pyignit:[0,2,3],pypi:3,pytest:3,python:[2,3,6,7,8],queri:[2,4,5,6],query_detail_metric_s:0,query_ent:0,query_id:[6,9],query_parallel:0,rais:2,random:6,rang:8,rare:2,raw:3,read_from_backup:0,read_only_al:8,read_only_saf:8,read_respons:7,read_write_al:8,read_write_saf:8,reason:6,rebalance_batch_s:0,rebalance_batches_prefetch_count:0,rebalance_delai:0,rebalance_mod:0,rebalance_ord:0,rebalance_throttl:0,rebalance_timeout:0,rebalancemod:8,recompil:3,recv:7,redi:[2,6],refer:2,referenc:6,remov:6,replic:8,repositori:3,repres:[2,6,8,9],represent:[2,6,8],request:[6,9],requir:3,resid:6,respect:2,respons:[2,6,9],result:[0,2,4,5],retriev:[2,6],rich:6,ridicul:8,right:2,room:6,run:3,runner:3,same:8,sampl:6,sample_hint:6,save:6,scale:3,search:1,send:7,sens:8,separ:8,sequenc:8,serial:[2,8],serializ:2,server:[2,6,9],set:6,setup:3,sever:2,shortarrai:8,shortarrayobject:[2,8],shortobject:[0,2,8],should:[3,6],sign:8,similar:[2,6],simpl:2,sinc:8,size:[2,8],smart:2,sneak:2,socket:[2,3,6,7],socketerror:[2,7],softwar:3,some:[2,3,5,9],someth:6,sophist:2,sort:8,sourc:[3,9],special:2,specif:8,specifi:6,speed:3,sphinx:3,split:[2,6],sql:[2,4,5],sql_escape_al:0,sql_index_inline_max_s:0,sql_schema:0,standard:[2,4,5],standard_typ:8,standardarrai:8,standardarrayobject:8,standardobject:8,start:[3,6],statistics_en:0,statu:[2,6],storag:6,store:[2,6,8],str:[2,6,8],stream:[2,3,8],string:[0,2,6,8],stringarrai:8,stringarrayobject:[2,8],struct:8,structarrai:8,structur:[1,6,7,8],stuck:3,style:[2,8],subject:6,submodul:4,subpackag:4,subset:6,success:[0,6],successfulli:6,suffic:2,summar:2,summari:2,support:6,sync:8,system:2,tabl:2,take:[0,8],tc_type:8,tcp:[3,6],tell:9,term:[3,6],test:1,than:8,them:2,therefor:8,thi:[2,3,5,6,8,9],those:[2,6],though:[2,8],three:2,through:[2,3],throughout:5,thu:2,tier:6,time:[2,3,8],timearrai:8,timearrayobject:[2,8],timedelta:[2,8],timeobject:[2,8],timestamp:2,timestamparrai:8,timestamparrayobject:[2,8],timestampobject:[2,8],to_python:[8,9],top:2,transact:3,translat:8,transpar:6,tricki:8,tupl:[2,5,6,8],two:[2,8],type:[1,2,5,6,8],type_cod:[2,4,5],type_id:8,type_or_id_nam:8,ultim:2,unclear:6,under:2,union:7,uniqu:8,univers:8,unknown:8,usag:1,use:[2,3,8],used:[5,6,8],useless:8,user:[2,3,8],uses:2,using:[6,8],utf:8,util:4,uuid:[2,8],uuidarrai:8,uuidarrayobject:[2,8],uuidobject:[2,8],valu:[1,2,5,6,8,9],value_hint:[0,6],vari:2,variabl:[2,8],variou:2,verbatim:6,verbos:2,veri:8,version:[2,3],version_major:7,version_minor:7,version_patch:7,view:6,virtualenv:3,wai:[6,8,9],want:[3,9],well:[2,6],what:[1,9],when:[2,6],whether:6,whic:6,which:6,whole:6,without:[2,3,6],word:8,work:8,workload:3,wrap:[2,6],wrapper:7,write_synchronization_mod:0,writer:6,writesynchronizationmod:8,written:[3,6],wrong:6,x01:8,x02:8,x03:8,x04:8,x05:8,x06:8,x07:8,x08:8,x0b:8,x0c:8,x0e:8,x0f:8,x10:8,x11:8,x12:8,x13:8,x14:8,x15:8,x16:8,x17:8,x18:8,x19:8,x1c:8,x1d:8,x1e:8,x1f:8,yet:[0,2,6],you:[2,3,6],your:[2,3],zero:6},titles:["Examples of usage","Welcome to Apache Ignite binary client Python API documentation!","Module Structure","Basic Information","pyignite","pyignite package","pyignite.api package","pyignite.connection package","pyignite.datatypes package","pyignite.queries package"],titleterms:{apach:1,api:[1,2,6],basic:3,binari:1,cach:0,cache_config:[6,8],cleanup:0,client:1,complex:8,configur:0,connect:[0,2,7],constant:5,creat:0,datatyp:[2,8],document:[1,3],edit:0,exampl:0,from:0,get:0,handshak:7,hint:0,ignit:1,indic:1,inform:3,inspect:0,instal:3,kei:0,key_valu:[6,8],licens:3,list:0,modul:[2,5,6,7,8,9],null_object:8,op_cod:9,open:0,packag:[5,6,7,8,9],prerequisit:3,primit:8,primitive_arrai:8,primitive_object:8,put:0,pyignit:[4,5,6,7,8,9],python:1,queri:9,result:6,sql:6,standard:8,structur:2,submodul:[5,6,7,8,9],subpackag:5,tabl:1,test:3,type:0,type_cod:8,usag:0,util:5,valu:0,welcom:1,what:3}})