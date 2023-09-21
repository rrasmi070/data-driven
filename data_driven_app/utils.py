import json


def check_dir(path,name):
    if name in path:
        return False

def make_hierarchy(df_objs, img_df):
    
    main_json = df_objs.to_json(orient='records')
    main_json = json.loads(main_json)

    
    rm_li = []
    for d in main_json:
        
        d["data"]= []
        imgs = img_df.loc[(img_df['parent_folder_id'] == d['id'])].to_json(orient='records') if len(img_df) > 0 else []
        d['files'] = json.loads(imgs) if imgs else []
    
    for i in range(len(main_json)-1):
        for j in range(i+1,len(main_json)):
            if main_json[j]["parent_folder"] == main_json[i]["id"]:
                main_json[i]['data'].append(main_json[j])
                rm_li.append(j)
            
    main_json = [main_json[i] for i in range(len(main_json)) if i not in rm_li]
        
                
    return main_json
    # def nested():
    #     if 0 < len(df_objs):
    #         id_list = df_objs[id].tolist()
            
    #         for i in id_list:
    #             nest = df_objs.loc[(id_list['parent_folder'] == i)]
    #             nest = nest.to_json(orient='records')
    #             df_2_json = json.loads(nest)
    #             # i['chield'] = df_2_json
                
    #             parent_df = df_objs.loc[(id_list['id'] == i)]
    #             parent = parent_df.to_json(orient='records')
    #             parentdf_2_json = json.loads(parent)
    #             parentdf_2_json['chield'] = df_2_json
    #             lists.append(i)
    #             nested(parent_df)
                
    #         return parent_df
            
    #     else:
    #         return []
    # nested(df_objs)