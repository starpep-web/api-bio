from __future__ import annotations
import os
import shutil
from typing import List
from abc import ABC, abstractmethod
from services.export.payload import SearchExportForm


_ASSETS_ROOT = os.path.abspath(os.getenv('ASSETS_LOCATION'))
_TMP_ARTIFACTS_ROOT = os.path.abspath(os.getenv('TEMP_ARTIFACTS_LOCATION'))


class _ResourceHandlers:
    class AbstractResourceHandler(ABC):
        @abstractmethod
        def get_source_directory(self) -> str:
            pass

        @abstractmethod
        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    class AttributeResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'attributes')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    class MetadataResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'metadata')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    class FastaResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'fasta')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    class EsmMeanResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'embeddings', 'esm-mean')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    class IFeatureAacResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'embeddings', 'ifeature-aac-20')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    class IFeatureDpcResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'embeddings', 'ifeature-dpc-400')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    class PdbResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'pdb')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pdb_output_directory = os.path.join(output_directory, 'pdb')
            os.mkdir(pdb_output_directory)
            print(f'Created PDB output directory: {pdb_output_directory}')

            source_directory = self.get_source_directory()

            for peptide_id in peptide_ids:
                pdb_file = os.path.join(source_directory, f'{peptide_id}.pdb')
                shutil.copy(pdb_file, pdb_output_directory)

            print(f'Copied {len(peptide_ids)} PDB files.')

    class HandlerFactory:
        @staticmethod
        def get(resource_name: str) -> _ResourceHandlers.AbstractResourceHandler:
            if resource_name == 'attributes':
                return _ResourceHandlers.AttributeResourceHandler()

            if resource_name == 'metadata':
                return _ResourceHandlers.MetadataResourceHandler()

            if resource_name == 'fasta':
                return _ResourceHandlers.FastaResourceHandler()

            if resource_name == 'esmMean':
                return _ResourceHandlers.EsmMeanResourceHandler()

            if resource_name == 'iFeatureAac':
                return _ResourceHandlers.IFeatureAacResourceHandler()

            if resource_name == 'iFeatureDpc':
                return _ResourceHandlers.IFeatureDpcResourceHandler()

            if resource_name == 'pdb':
                return _ResourceHandlers.PdbResourceHandler()

            raise ValueError('Invalid resource_name provided to AbstractHandlerFactory.')


def create_zip_archive(file_name: str, peptide_ids: List[str], form: SearchExportForm) -> None:
    if not file_name.endswith('.zip'):
        file_name += '.zip'

    exportable_resources = form.get_exportable_resources()
    if len(exportable_resources) < 1:
        raise Exception('At least one resource needs to be exported to create an archive.')

    output_directory = os.path.join(_TMP_ARTIFACTS_ROOT, f'{file_name}.d')
    os.mkdir(output_directory)
    print(f'Created artifact directory: {output_directory}')

    for resource in exportable_resources:
        handler = _ResourceHandlers.HandlerFactory.get(resource)
        handler.create_resource_artifact(output_directory, peptide_ids)
