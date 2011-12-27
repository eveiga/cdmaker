# -*- coding: utf-8 -*-
import logging

logging.basicConfig(
    filename='execution.log',
    format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Execution logger')
