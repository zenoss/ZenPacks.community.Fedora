import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.FedoraMonitor')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def findFedora(dmd):
    return dmd.findChild('Devices/Server/SSH/Linux/Fedora')

class ZenPack(ZenPackBase):

    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Linux/Fedora
        """
        try:
            fedora = findFedora(app.dmd)
        except Exception, e:
            import traceback
            log.debug(traceback.format_exc())
            raise Exception('Device class Server/SSH/Linux/Fedora does not exist. '
                            'Cannot install Fedora ZenPack.')
        ZenPackBase.install(self, app)

        plugins=[]
        for plugin in fedora.zCollectorPlugins:
            if plugin != "zenoss.cmd.uname_a":
                plugins.append(plugin)
            else:
                plugins.append('zenoss.cmd.linux.fedora_uname_a')

        plugins.append('zenoss.cmd.linux.fedora_rpm')

        fedora.setZenProperty( 'zCollectorPlugins', plugins )

        fedora.register_devtype('Fedora Server', 'SSH')

    def remove(self, app, leaveObjects=False):
        """
        Remove the collector plugins.
        """
        ZenPackBase.remove(self, app, leaveObjects)
        fedora = findFedora(app.dmd)
        if not leaveObjects:
            newlist=[]
            for plugin in fedora.zCollectorPlugins:
                if plugin == "zenoss.cmd.linux.eix":
                    pass
                elif plugin == "zenoss.cmd.linux.fedora_uname_a":
                    newlist.append("zenoss.cmd.uname_a")
                else:
                    newlist.append(plugin)

            fedora.zCollectorPlugins = newlist
