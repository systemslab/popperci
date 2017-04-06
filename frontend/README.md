web2py-based frontend of PopperCI. To launch the site:

```bash
docker run -d \
  -e WEB2PY_ADMIN=Pa55word! \
  -p 80:80 \
  -v `pwd`/frontend:/opt/web2py/applications/popperci \
  -v `pwd`/logs:/var/log/nginx \
  --name web2py \
  madharjan/docker-nginx-web2py-min:2.14.6
```
