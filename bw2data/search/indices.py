from .schema import bw2_schema
from .. import config, Database
from whoosh import index


class IndexManager(object):
    def __init__(self, dir_name=u"whoosh"):
        self.path = config.request_dir(u"whoosh")

    def get(self):
        try:
            return index.open_dir(self.path)
        except index.EmptyIndexError:
            return self.create()

    def create(self):
        return index.create_in(self.path, bw2_schema)

    def reset(self):
        return self.create()

    def _format_dataset(self, ds):
        return dict(
            name=ds.get(u"name", u""),
            comment=ds.get(u"comment", u""),
            product=ds.get(u"reference product", u""),
            categories=u", ".join(ds.get(u"categories", [])),
            location=ds.get(u"location", u""),
            database=ds[u"database"],
            key=u":".join((ds[u'database'], ds[u'code']))
        )

    def add_dataset(self, ds):
        writer = self.get().writer()
        writer.add_document(**self._format_dataset(ds))
        writer.commit()

    def add_datasets(self, datasets):
        writer = self.get().writer()
        for ds in datasets:
            writer.add_document(**self._format_dataset(ds))
        writer.commit()

    def update_dataset(self):
        pass

    def delete_dataset(self):
        pass