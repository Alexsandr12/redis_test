from check_domains import check_domains, check_one_domain, redis_conn


dnames = (input("Введите имя домена или список доменов через пробел: ").split())
if len(dnames) == 1:
    dname = dnames[0]
    print(check_one_domain(dname))
    print(redis_conn.ttl(dname))
elif len(dnames) >= 1:
    print(check_domains(dnames))
else:
    print("Домены не найдены")
