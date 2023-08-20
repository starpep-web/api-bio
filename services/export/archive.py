from __future__ import annotations
import os
import shutil
from typing import List
from abc import ABC, abstractmethod
from services.export.payload import SearchExportForm


_ASSETS_ROOT = os.path.abspath(os.getenv('ASSETS_LOCATION'))
_TMP_ARTIFACTS_ROOT = os.path.abspath(os.getenv('TEMP_ARTIFACTS_LOCATION'))
_ARTIFACT_NAME_PREFIX = 'StarPep-exported'


class _ResourceHandlers:
    class AbstractResourceHandler(ABC):
        @abstractmethod
        def get_source_directory(self) -> str:
            pass

        @abstractmethod
        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pass

    @staticmethod
    def create_resource_csv_artifact(output_file: str, source_directory: str, peptide_ids: List[str]) -> None:
        with open(output_file, 'w') as output_file:
            for index, peptide_id in enumerate(peptide_ids):
                csv_input_file = os.path.join(source_directory, f'{peptide_id}.csv')

                with open(csv_input_file, 'r') as input_file:
                    if index == 0:
                        input_content = input_file.read()
                    else:
                        input_file.readline()  # Skip the columns header since it was already added before.
                        input_content = input_file.readline()

                    output_file.write(input_content)

    class AttributeResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'attributes')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            csv_output_file = os.path.join(output_directory, f'{_ARTIFACT_NAME_PREFIX}-features.csv')
            _ResourceHandlers.create_resource_csv_artifact(csv_output_file, self.get_source_directory(), peptide_ids)
            print(f'Created Attributes CSV file with {len(peptide_ids)} entries: {csv_output_file}')

    class MetadataResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'metadata')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            csv_output_file = os.path.join(output_directory, f'{_ARTIFACT_NAME_PREFIX}-metadata.csv')
            _ResourceHandlers.create_resource_csv_artifact(csv_output_file, self.get_source_directory(), peptide_ids)
            print(f'Created Metadata CSV file with {len(peptide_ids)} entries: {csv_output_file}')

    class FastaResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'fasta')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            fasta_output_file = os.path.join(output_directory, f'{_ARTIFACT_NAME_PREFIX}.fasta')

            with open(fasta_output_file, 'w') as output_file:
                source_directory = self.get_source_directory()

                for peptide_id in peptide_ids:
                    fasta_input_file = os.path.join(source_directory, f'{peptide_id}.fasta')

                    with open(fasta_input_file, 'r') as input_file:
                        input_content = input_file.read()
                        output_file.write(input_content)

            print(f'Created FASTA file with {len(peptide_ids)} entries: {fasta_output_file}')

    class EsmMeanResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'embeddings', 'esm-mean')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            csv_output_file = os.path.join(output_directory, f'{_ARTIFACT_NAME_PREFIX}-embeddings-esm-mean.csv')
            _ResourceHandlers.create_resource_csv_artifact(csv_output_file, self.get_source_directory(), peptide_ids)
            print(f'Created Embeddings ESM-mean CSV file with {len(peptide_ids)} entries: {csv_output_file}')

    class IFeatureAacResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'embeddings', 'ifeature-aac-20')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            csv_output_file = os.path.join(output_directory, f'{_ARTIFACT_NAME_PREFIX}-embeddings-ifeature-aac-20.csv')
            _ResourceHandlers.create_resource_csv_artifact(csv_output_file, self.get_source_directory(), peptide_ids)
            print(f'Created Embeddings iFeature-AAC CSV file with {len(peptide_ids)} entries: {csv_output_file}')

    class IFeatureDpcResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'csv', 'embeddings', 'ifeature-dpc-400')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            csv_output_file = os.path.join(output_directory, f'{_ARTIFACT_NAME_PREFIX}-embeddings-ifeature-dpc-400.csv')
            _ResourceHandlers.create_resource_csv_artifact(csv_output_file, self.get_source_directory(), peptide_ids)
            print(f'Created Embeddings iFeature-DPC CSV file with {len(peptide_ids)} entries: {csv_output_file}')

    class PdbResourceHandler(AbstractResourceHandler):
        def get_source_directory(self) -> str:
            return os.path.join(_ASSETS_ROOT, 'peptides', 'pdb')

        def create_resource_artifact(self, output_directory: str, peptide_ids: List[str]) -> None:
            pdb_output_directory = os.path.join(output_directory, 'pdb')
            os.mkdir(pdb_output_directory)

            source_directory = self.get_source_directory()

            for peptide_id in peptide_ids:
                pdb_file = os.path.join(source_directory, f'{peptide_id}.pdb')
                shutil.copy(pdb_file, pdb_output_directory)

            print(f'Created PDB output directory with {len(peptide_ids)} entries: {pdb_output_directory}')

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


def _make_zip_archive(source_directory: str, destination_file: str) -> None:
    shutil.make_archive(
        base_name=destination_file,
        format='zip',
        root_dir=source_directory,
        base_dir='.'
    )

def create_zip_archive(file_name: str, peptide_ids: List[str], form: SearchExportForm) -> None:
    exportable_resources = form.get_exportable_resources()
    if len(exportable_resources) < 1:
        raise Exception('At least one resource needs to be exported to create an archive.')

    if len(peptide_ids) < 1:
        raise ValueError('At least one peptide needs to be exported.')

    artifact_archive_filename = os.path.join(_TMP_ARTIFACTS_ROOT, file_name)
    artifact_directory = os.path.join(_TMP_ARTIFACTS_ROOT, f'{file_name}.d')
    os.mkdir(artifact_directory)
    print(f'Created artifact directory: {artifact_directory}')

    try:
        for resource in exportable_resources:
            handler = _ResourceHandlers.HandlerFactory.get(resource)
            handler.create_resource_artifact(artifact_directory, peptide_ids)

        _make_zip_archive(artifact_directory, artifact_archive_filename)
        print(f'Created artifact archive: {artifact_archive_filename}')
    except Exception as e:
        artifact_archive_filename += '.zip'

        if os.path.exists(artifact_archive_filename):
            os.remove(artifact_archive_filename)
            print(f'Removed artifact archive: {artifact_archive_filename}')

        raise e
    finally:
        shutil.rmtree(artifact_directory)
        print(f'Removed artifact directory: {artifact_directory}')
