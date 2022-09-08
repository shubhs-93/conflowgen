from __future__ import annotations

import copy
from typing import Dict

from conflowgen.domain_models.container import Container
from conflowgen.domain_models.data_types.container_length import ContainerLength
from conflowgen.domain_models.data_types.mode_of_transport import ModeOfTransport
from conflowgen.analyses.abstract_analysis import AbstractAnalysis
from conflowgen.descriptive_datatypes import ContainerVolumeFromOriginToDestination


class ContainerFlowByVehicleTypeAnalysis(AbstractAnalysis):
    """
    This analysis can be run after the synthetic data has been generated.
    The analysis returns a data structure that can be used for generating reports (e.g., in text or as a figure)
    as it is the case with :class:`.ContainerFlowByVehicleTypeAnalysisReport`.
    """

    @staticmethod
    def get_inbound_to_outbound_flow() -> ContainerVolumeFromOriginToDestination:
        """
        This is the overview of the generated inbound to outbound container flow by vehicle type.
        """
        inbound_to_outbound_flow_in_containers: Dict[ModeOfTransport, Dict[ModeOfTransport, float]] = {
            vehicle_type_inbound:
                {
                    vehicle_type_outbound: 0
                    for vehicle_type_outbound in ModeOfTransport
                }
            for vehicle_type_inbound in ModeOfTransport
        }
        inbound_to_outbound_flow_in_teu = copy.deepcopy(inbound_to_outbound_flow_in_containers)

        container: Container
        for container in Container.select():
            inbound_vehicle_type = container.delivered_by
            outbound_vehicle_type = container.picked_up_by
            inbound_to_outbound_flow_in_containers[inbound_vehicle_type][outbound_vehicle_type] += 1
            inbound_to_outbound_flow_in_teu[inbound_vehicle_type][outbound_vehicle_type] += \
                ContainerLength.get_factor(container.length)

        inbound_to_outbound_flow = ContainerVolumeFromOriginToDestination(
            containers=inbound_to_outbound_flow_in_containers,
            teu=inbound_to_outbound_flow_in_teu
        )

        return inbound_to_outbound_flow
