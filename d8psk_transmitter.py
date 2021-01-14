#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: pentoo
# GNU Radio version: 3.8.2.0

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation


class d8psk_transmitter(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Variables
        ##################################################
        self.throttle_rate = throttle_rate = 320000
        self.samp_rate = samp_rate = 1190550
        self.constellation_9PSK_auto = constellation_9PSK_auto = digital.constellation_calcdist([0.383+0.924j, 0.924+0.383j, 0.924-0.383j, 0.383-0.924j, -0.383-0.924j, -0.924-0.383j, -0.924+0.383j, -0.383+0.924j, 0], [1,0,7,6,5,4,3,2,8],
        8, 1).base()
        self.constellation_9PSK_auto.gen_soft_dec_lut(8)

        ##################################################
        # Blocks
        ##################################################
        self.digital_map_bb_0_0_0 = digital.map_bb([6,7,0,1,2,3,4,5,8])
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=constellation_9PSK_auto,
            differential=False,
            samples_per_symbol=4,
            pre_diff_code=True,
            excess_bw=0.35*3,
            verbose=False,
            log=False)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('/home/pentoo/defcon27_badge_sdr/trans_output.wav', 2, samp_rate, 16)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(3)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, throttle_rate,True)
        self.blocks_skiphead_1_0 = blocks.skiphead(gr.sizeof_float*1, 80)
        self.blocks_skiphead_1 = blocks.skiphead(gr.sizeof_float*1, 80)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 1)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, 4)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(.7)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/pentoo/defcon27_badge_sdr/signal.bin', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_divide_xx_0 = blocks.divide_ss(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, 85+4+1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_short_0 = blocks.char_to_short(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ss(1)
        self.analog_const_source_x_0 = analog.sig_source_s(0, analog.GR_CONST_WAVE, 0, 0, -8*256)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.blocks_char_to_short_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_char_to_short_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.digital_map_bb_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_skiphead_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_skiphead_1_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_skiphead_1, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_skiphead_1_0, 0), (self.blocks_wavfile_sink_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_map_bb_0_0_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))


    def get_throttle_rate(self):
        return self.throttle_rate

    def set_throttle_rate(self, throttle_rate):
        self.throttle_rate = throttle_rate
        self.blocks_throttle_0.set_sample_rate(self.throttle_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_constellation_9PSK_auto(self):
        return self.constellation_9PSK_auto

    def set_constellation_9PSK_auto(self, constellation_9PSK_auto):
        self.constellation_9PSK_auto = constellation_9PSK_auto





def main(top_block_cls=d8psk_transmitter, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
