from zope.interface import Interface
from Products.Five.browser import BrowserView
from plone import api
from plone.restapi.behaviors import IBlocks
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection

import uuid


class BlocksUUIDFixer(BrowserView):
    """ """

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        brains = api.content.find(object_provides=IBlocks.__identifier__)
        output = []

        for brain in brains:
            obj = brain.getObject()
            blocks = obj.blocks
            blocks_layout = obj.blocks_layout["items"]

            new_blocks = {}
            new_blocks_layout = {"items": []}
            for uid in blocks_layout:
                newuuid = str(uuid.uuid4())
                new_blocks.update({newuuid: blocks[uid]})
                new_blocks_layout["items"].append(newuuid)

                output.append(
                    "Fixed UUID {} -> {} in {}\n".format(
                        uid, newuuid, obj.absolute_url()
                    )
                )
            obj.blocks = new_blocks
            obj.blocks_layout = new_blocks_layout

            output.append("\n")
            output.append(
                "New blocks {} \nfor {}\n".format(obj.absolute_url(), new_blocks)
            )
            output.append(
                "New layout {} \nfor {}\n".format(obj.absolute_url(), new_blocks_layout)
            )

        return "".join(output)
