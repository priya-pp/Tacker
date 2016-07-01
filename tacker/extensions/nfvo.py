# Copyright 2016 Brocade Communications Systems Inc
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import six

from tacker.api import extensions
from tacker.api.v1 import attributes as attr
from tacker.api.v1 import resource_helper
from tacker.common import exceptions
from tacker.extensions.base_plugins import vnffg
from tacker.plugins.common import constants


class VimUnauthorizedException(exceptions.TackerException):
    message = _("%(message)s")


class VimConnectionException(exceptions.TackerException):
    message = _("%(message)s")


class VimInUseException(exceptions.TackerException):
    message = _("VIM %(vim_id)s is still in use by VNF")


# Deprecated. Will be removed in Ocata release
class VimDefaultNameNotDefined(exceptions.TackerException):
    message = _("Default VIM is not set. Either specify a"
                " valid VIM during the VNF creation or set default VIM"
                " in tacker.conf")


# Deprecated. Will be removed in Ocata release
class VimDefaultIdException(exceptions.TackerException):
    message = _("Default VIM name %(vim_name)s is invalid or there are "
                "multiple VIM matches found. Please specify a valid default "
                "VIM in tacker.conf")


class VimDefaultDuplicateException(exceptions.TackerException):
    message = _("Default VIM already exists %(vim_id)s.")


class VimNotFoundException(exceptions.TackerException):
    message = _("Specified VIM id %(vim_id)s is invalid. Please verify and "
                "pass a valid VIM id")


class VimRegionNotFoundException(exceptions.TackerException):
    message = _("Unknown VIM region name %(region_name)s")


class VimKeyNotFoundException(exceptions.TackerException):
    message = _("Unable to find key file for VIM %(vim_id)s")


class VimDuplicateUrlException(exceptions.TackerException):
    message = _("VIM with specified auth URL already exists. Cannot register "
                "duplicate VIM")


class VimPorjectDomainNameMissingException(exceptions.TackerException):
    message = _("'project_domain_name' is missing")


class VimUserDomainNameMissingException(exceptions.TackerException):
    message = _("'user_domain_name' is missing")


class VnffgdVnfdNotFoundException(exceptions.NotFound):
    message = _("Specified VNFD %(vnfd_name)s in VNFFGD does not exist. "
                "Please create VNFDs before creating VNFFG")


class VnffgdVnfNotFoundException(exceptions.NotFound):
    message = _("Matching VNF Instance for VNFD %(vnfd_name)s could not be "
                "found. Please create an instance before creating VNFFG.")


class VnffgdCpNotFoundException(exceptions.NotFound):
    message = _("Specified CP %(cp_id)s could not be found in VNFD "
                "%(vnfd_name)s. Please check VNFD for correct Connection "
                "Point.")


class VnffgdCpNoForwardingException(exceptions.TackerException):
    message = _("Specified CP %(cp_id)s in VNFD %(vnfd_name)s "
                "does not have forwarding capability, which is required to be "
                "included in forwarding path")


class VnffgdInUse(exceptions.InUse):
    message = _('VNFFGD %(vnffgd_id)s is still in use')


class VnffgdNotFound(exceptions.NotFound):
    message = _('VNFFG Template %(vnffgd_id)s could not be found')


class VnffgCreateFailed(exceptions.TackerException):
    message = _('Creating VNFFG based on %(vnffd_id)s failed')


class VnffgInvalidMappingException(exceptions.TackerException):
    message = _("Matching VNF Instance for VNFD %(vnfd_name)s could not be "
                "found. Please create an instance before creating VNFFG.")


class VnffgPropertyNotFound(exceptions.NotFound):
    message = _('VNFFG Property %(vnffg_property)s could not be found')


class VnffgCpNotFoundException(exceptions.NotFound):
    message = _("Specified CP %(cp_id)s could not be found in VNF "
                "%(vnf_id)s.")


class VnffgNotFound(exceptions.NotFound):
    message = _('VNFFG %(vnffg_id)s could not be found')


class VnffgInUse(exceptions.InUse):
    message = _('VNFFG %(vnffg_id)s is still in use')


class VnffgVnfNotFound(exceptions.NotFound):
    message = _("Specified VNF instance %(vnf_name)s in VNF Mapping could not "
                "be found")


class VnffgDeleteFailed(exceptions.TackerException):
    message = _('Deleting VNFFG %(vnffg_id)s failed')


class NfpAttributeNotFound(exceptions.NotFound):
    message = _('NFP attribute %(attribute)s could not be found')


class NfpNotFound(exceptions.NotFound):
    message = _('NFP %(nfp_id)s could not be found')


class NfpInUse(exceptions.InUse):
    message = _('NFP %(nfp_id)s is still in use')


class NfpPolicyCriteriaError(exceptions.PolicyCheckError):
    message = _('%(error)s in policy')


class NfpPolicyNotFound(exceptions.NotFound):
    message = _('Policy not found in NFP %(nfp)s')


class NfpPolicyTypeError(exceptions.PolicyCheckError):
    message = _('Unsupported Policy Type: %(type)s')


class NfpForwarderNotFound(exceptions.NotFound):
    message = _('VNFD Forwarder %(vnfd)s not found in VNF Mapping %(mapping)s')


class NfpRequirementsException(exceptions.TackerException):
    message = _('VNFD Forwarder %(vnfd) specified more than twice in '
                'requirements path')


class SfcInUse(exceptions.InUse):
    message = _('SFC %(sfc_id)s is still in use')


class SfcNotFound(exceptions.NotFound):
    message = _('Service Function Chain %(sfc_id)s could not be found')


class ClassifierInUse(exceptions.InUse):
    message = _('Classifier %(classifier_id)s could not be found')


class ClassifierNotFound(exceptions.NotFound):
    message = _('Classifier %(classifier_id)s could not be found')


RESOURCE_ATTRIBUTE_MAP = {

    'vims': {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'primary_key': True,
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True
        },
        'type': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': None},
            'is_visible': True
        },
        'auth_url': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': None},
            'is_visible': True
        },
        'auth_cred': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:dict_or_nodata': None},
            'is_visible': True,
        },
        'vim_project': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:dict_or_nodata': None},
            'is_visible': True,
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True,
        },
        'description': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True,
            'default': '',
        },
        'status': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:string': None},
            'is_visible': True,
        },
        'placement_attr': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'default': None,
        },
        'shared': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': False,
            'convert_to': attr.convert_to_boolean,
            'required_by_policy': True
        },
        'is_default': {
            'allow_post': True,
            'allow_put': True,
            'is_visible': True,
        },
    },

    'vnffgds': {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'primary_key': True,
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True,
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True,
        },
        'description': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True,
            'default': '',
        },
        'attributes': {
            'allow_post': True,
            'allow_put': False,
            'convert_to': attr.convert_none_to_empty_dict,
            'validate': {'type:dict_or_nodata': None},
            'is_visible': True,
            'default': None,
        },
    },

    'vnffgs': {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True
        },
        'vnffgd_id': {
            'allow_post': True,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'name': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True,
        },
        'description': {
            'allow_post': True,
            'allow_put': True,
            'validate': {'type:string': None},
            'is_visible': True,
            'default': '',
        },
        'vnf_mapping': {
            'allow_post': True,
            'allow_put': False,
            'convert_to': attr.convert_none_to_empty_dict,
            'validate': {'type:dict_or_nodata': None},
            'is_visible': True,
            'default': None,
        },
        'symmetrical': {
            'allow_post': True,
            'allow_put': False,
            'is_visible': True,
            'validate': {'type:boolean': None},
            'default': False,
        },
        'forwarding_paths': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
        'status': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
    },

    'nfps': {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True
        },
        'vnffg_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'name': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:string': None},
            'is_visible': True,
        },
        'classifier_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'chain_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'path_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:string': None},
            'is_visible': True,
        },
        'symmetrical': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'validate': {'type:boolean': None},
            'default': False,
        },
        'status': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
    },
    'sfcs': {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True
        },
        'nfp_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'instance_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'chain': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
        'path_id': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
        'symmetrical': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
            'validate': {'type:boolean': None},
            'default': False,
        },
        'status': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
    },
    'classifiers': {
        'id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
            'primary_key': True
        },
        'tenant_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:string': None},
            'required_by_policy': True,
            'is_visible': True
        },
        'nfp_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'instance_id': {
            'allow_post': False,
            'allow_put': False,
            'validate': {'type:uuid': None},
            'is_visible': True,
        },
        'match': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
        'chain_id': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
        'status': {
            'allow_post': False,
            'allow_put': False,
            'is_visible': True,
        },
    },
}


class Nfvo(extensions.ExtensionDescriptor):
    @classmethod
    def get_name(cls):
        return 'NFV Orchestrator'

    @classmethod
    def get_alias(cls):
        return 'NFVO'

    @classmethod
    def get_description(cls):
        return "Extension for NFV Orchestrator"

    @classmethod
    def get_namespace(cls):
        return 'http://wiki.openstack.org/Tacker'

    @classmethod
    def get_updated(cls):
        return "2015-12-21T10:00:00-00:00"

    @classmethod
    def get_resources(cls):
        special_mappings = {}
        plural_mappings = resource_helper.build_plural_mappings(
            special_mappings, RESOURCE_ATTRIBUTE_MAP)
        attr.PLURALS.update(plural_mappings)
        return resource_helper.build_resource_info(
            plural_mappings, RESOURCE_ATTRIBUTE_MAP, constants.NFVO,
            translate_name=True)

    @classmethod
    def get_plugin_interface(cls):
        return NFVOPluginBase

    def update_attributes_map(self, attributes):
        super(Nfvo, self).update_attributes_map(
            attributes, extension_attrs_map=RESOURCE_ATTRIBUTE_MAP)

    def get_extended_resources(self, version):
        version_map = {'1.0': RESOURCE_ATTRIBUTE_MAP}
        return version_map.get(version, {})


@six.add_metaclass(abc.ABCMeta)
class NFVOPluginBase(vnffg.VNFFGPluginBase):
    def get_plugin_name(self):
        return constants.NFVO

    def get_plugin_type(self):
        return constants.NFVO

    def get_plugin_description(self):
        return 'Tacker NFV Orchestrator plugin'

    @abc.abstractmethod
    def create_vim(self, context, vim):
        pass

    @abc.abstractmethod
    def delete_vim(self, context, vim_id):
        pass

    @abc.abstractmethod
    def get_vim(self, context, vim_id, fields=None, mask_password=True):
        pass

    @abc.abstractmethod
    def get_vims(self, context, filters=None, fields=None):
        pass

    def get_vim_by_name(self, context, vim_name, fields=None,
                        mask_password=True):
        raise NotImplementedError()

    def get_default_vim(self, context):
        raise NotImplementedError()
