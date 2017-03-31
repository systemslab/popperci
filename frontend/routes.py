# makes the PopperCI application the default application inside web2py
# (e.g. no need to type 127.0.0.1:8000/popperci/default/index)
routers = dict(
    BASE=dict(
        default_application='popperci',
    )
)
