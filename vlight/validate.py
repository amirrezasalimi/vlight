import re


def parseOptions(val):
    out = {}
    for v in val.split("|"):
        vPart = v.split(":")
        out[vPart[0]] = (vPart[1].split(",") if len(vPart[1].split(",")) > 1 else vPart[1]) if len(vPart) > 1 else ""
    return out


def cleanData(value):
    return value


class error:
    errors = {}

    def first(self, _key):
        if _key in self.errors:
            return self.errors[_key][0]
        return None

    def last(self, _key):
        if _key in self.errors:
            return self.errors[_key][-1]
        return None

    def get(self, _key, _len=1):
        return self.errors[_key][0, _len] if _key in self.errors else []

    def all(self):
        errors = []
        for k, v in self.errors.items():
            for _err_val in v:
                errors.append(_err_val)
        return errors

    def has(self, _k):
        return _k in self.errors


class validate:
    data = {}
    schema = {}
    _errors = {}
    messages = {
        "required": "field {field} required",
        "email": " {field} is not valid ",
        "text": "{field} is not valid text",
        "int": "{field} is not valid integer",
        "str.min": "{field} is smaller than {min} character",
        "str.max": "{field} is bigger than {value} character",
        "int.min": "{field} is smaller than {min} ",
        "int.max": "{field} is bigger than {value} ",
        "regex": "{field} is not valid data"
    }
    filters = {}
    user_messages = {}

    def __init__(self, schema, **kwargs):
        self.schema = schema
        if 'data' in kwargs:
            self.data = kwargs.get("data")
        if 'messages' in kwargs:
            self.user_messages = kwargs.get("messages")

    @staticmethod
    def add_filter(name, check, includes=""):
        validate.filters[name] = [check, includes]

    def add_error(self, _key, _msg_key, options, args):
        if _key not in self._errors:
            self._errors[_key] = []
        self._errors[_key].append(self.get_message(options, _msg_key).format(**args))

    def error(self, _key):
        if _key in self._errors:
            return self._errors[_key]
        return []

    def has_error(self, _key):
        r = self.error(_key)
        return r if len(r) > 0 else False

    def check(self):
        data = self.data
        self._errors = {}
        for k, v in self.schema.items():
            op = parseOptions(v) if type(v) == str else v
            val = data[k] if k in data else None

            args = {
                "field": k,
                "value": val,
                "v": val,
                "f": k,

                **op
            }

            def error(err_title):
                self.add_error(k, err_title, op, args)

            filters = self.filters
            for _k, _v in filters.items():
                check = _v[0]
                includes = _v[1]
                if includes != "":
                    v += "|" + includes
                if _k in op:
                    check(_k, val, op[_k], error)
                    op = parseOptions(v) if type(v) == str else v

            if k not in data:
                if ('req' in op) or ('required' in op):
                    error("required")
            else:
                if ('req' in op) or ('required' in op):
                    if val == "":
                        error("required")
                        continue
                if 'email' in op:
                    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", val) or type(val) is not str:
                        error("email")
                if 'ip' in op:
                    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", val) or type(val) is not str:
                        error("ip")

                if "url" in op:
                    if not re.match(
                            r"^http(s?):\/\/(www\.)?(((\w+(([\.\-]{1}([a-z]{2,})+)+)(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*$)|(\w+((\.([a-z]{2,})+)+)(\:[0-9]{1,5}(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*$)))|(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(([0-9]|([1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]+)+)(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*)((\:[0-9]{1,5}(\/[a-zA-Z0-9\_\=\?\&\.\#\-\W]*)*$)*))$",
                            val) or type(val) is not str:
                        error("url")

                if 'regex' in op:
                    if not re.match(op["regex"], val):
                        error("regex")
                if 'not_regex' in op:
                    if re.match(op["not_regex"], val):
                        error("not_regex")
                if ('string' in op) or ("text" in op):
                    if type(val) is not str:
                        error("text")

                if ('int' in op) and not val.isdigit():
                    error("int")

                if type(val) in (str, int) and "int" not in op:
                    if "min" in op:
                        _min = int(op["min"])
                        if len(val) < _min:
                            error("str.min")
                    if "max" in op:
                        _max = int(op["max"])
                        if len(val) > _max:
                            error("str.max")

                if 'int' in op:
                    if "min" in op:
                        _min = int(op["min"])
                        if val < _min:
                            error("int.min")
                    if "max" in op:
                        _max = int(op["max"])
                        if val > _max:
                            error("int.max")

                if "in" in op and val not in op["in"]:
                    error("in")

                if "not_in" in op and val in op["in"]:
                    error("not_in")
                if "between" in op:
                    between = op["between"]
                    _min = int(between[0])
                    _max = int(between[1])
                    if (val < _min) or (val > _max):
                        error("between")

    def get_message(self, options, name):
        if name is not None:
            if name + ".msg" in options:
                return options[name + ".msg"]
            if name in self.user_messages:
                return self.user_messages[name]
            if name in self.messages:
                return self.messages[name]
            return name

    def get(self, name):
        return cleanData(self.data[name])

    def isOk(self):
        self.check()
        return len(self._errors) == 0

    def fails(self):
        self.check()
        return len(self._errors) > 0

    def errors(self):
        err = error()
        err.errors = self._errors
        return err

    def form(self):
        # create html5 form
        # coming soon
        pass


def check_extension(field, value, attr, error):
    from pathlib import Path
    if type(value) is str:
        ext = Path(value).suffix.replace(".", "")
        if ext not in attr:
            error("extension '.%s' is not valid" % ext)


validate.add_filter("ext", check_extension, "req")
