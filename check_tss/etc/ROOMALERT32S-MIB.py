#
# PySNMP MIB module ROOMALERT32S-MIB (http://snmplabs.com/pysmi)
# ASN.1 source file:///usr/share/snmp/mibs/ROOMALERT32S.MIB
# Produced by pysmi-1.1.12 at Tue Dec  3 22:34:34 2024
# On host admin platform Linux version 5.15.0-89-generic by user root
# Using Python version 3.10.12 (main, Sep 11 2024, 15:47:36) [GCC 11.4.0]
#
Integer, OctetString, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueRangeConstraint, ValueSizeConstraint, ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ValueSizeConstraint", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint")
ModuleCompliance, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
enterprises, Bits, MibIdentifier, TimeTicks, Unsigned32, Integer32, Counter32, Counter64, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, IpAddress, NotificationType, ModuleIdentity, ObjectIdentity = mibBuilder.importSymbols("SNMPv2-SMI", "enterprises", "Bits", "MibIdentifier", "TimeTicks", "Unsigned32", "Integer32", "Counter32", "Counter64", "Gauge32", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "iso", "IpAddress", "NotificationType", "ModuleIdentity", "ObjectIdentity")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
avtech = MibIdentifier((1, 3, 6, 1, 4, 1, 20916))
products = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1))
roomalert32S = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11))
sensors = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1))
internal = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1))
temperature = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 1))
humidity = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 2))
power = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 3))
heat_index = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 4)).setLabel("heat-index")
analog = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 5))
relay = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 6))
dew_point = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 7)).setLabel("dew-point")
digital = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2))
digital_sen1 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1)).setLabel("digital-sen1")
digital_sen2 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2)).setLabel("digital-sen2")
digital_sen3 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3)).setLabel("digital-sen3")
digital_sen4 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4)).setLabel("digital-sen4")
digital_sen5 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5)).setLabel("digital-sen5")
digital_sen6 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6)).setLabel("digital-sen6")
digital_sen7 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7)).setLabel("digital-sen7")
digital_sen8 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8)).setLabel("digital-sen8")
switch = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3))
traps = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 2))
externalrelays = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3))
externalrelay1 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1))
externalrelay2 = MibIdentifier((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2))
internal_tempf = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-tempf").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_tempf.setStatus('mandatory')
internal_tempc = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-tempc").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_tempc.setStatus('mandatory')
internal_humidity = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 2, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-humidity").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_humidity.setStatus('mandatory')
internal_heat_index = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 4, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-heat-index").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_heat_index.setStatus('optional')
internal_heat_indexC = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 4, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-heat-indexC").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_heat_indexC.setStatus('optional')
internal_power = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 3, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("internal-power").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_power.setStatus('mandatory')
internal_analog1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 5, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-analog1").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_analog1.setStatus('mandatory')
internal_analog2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 5, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-analog2").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_analog2.setStatus('mandatory')
internal_relay1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 6, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("internal-relay1").setMaxAccess("readwrite")
if mibBuilder.loadTexts: internal_relay1.setStatus('mandatory')
internal_relay2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 6, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("internal-relay2").setMaxAccess("readwrite")
if mibBuilder.loadTexts: internal_relay2.setStatus('mandatory')
internal_dew_point_c = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 7, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-dew-point-c").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_dew_point_c.setStatus('optional')
internal_dew_point_f = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 1, 7, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("internal-dew-point-f").setMaxAccess("readonly")
if mibBuilder.loadTexts: internal_dew_point_f.setStatus('optional')
digital_sen1_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen1-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen1_1.setStatus('mandatory')
digital_sen1_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen1-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen1_2.setStatus('mandatory')
digital_sen1_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen1-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen1_3.setStatus('mandatory')
digital_sen1_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen1-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen1_4.setStatus('mandatory')
digital_sen1_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen1-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen1_5.setStatus('mandatory')
digital_sen1_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen1-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen1_6.setStatus('mandatory')
digital_sen1_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen1-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen1_7.setStatus('mandatory')
digital_sen2_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen2-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen2_1.setStatus('mandatory')
digital_sen2_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen2-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen2_2.setStatus('mandatory')
digital_sen2_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen2-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen2_3.setStatus('mandatory')
digital_sen2_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen2-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen2_4.setStatus('mandatory')
digital_sen2_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen2-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen2_5.setStatus('mandatory')
digital_sen2_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen2-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen2_6.setStatus('mandatory')
digital_sen2_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 2, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen2-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen2_7.setStatus('mandatory')
digital_sen3_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen3-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen3_1.setStatus('mandatory')
digital_sen3_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen3-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen3_2.setStatus('mandatory')
digital_sen3_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen3-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen3_3.setStatus('mandatory')
digital_sen3_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen3-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen3_4.setStatus('mandatory')
digital_sen3_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen3-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen3_5.setStatus('mandatory')
digital_sen3_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen3-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen3_6.setStatus('mandatory')
digital_sen3_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 3, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen3-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen3_7.setStatus('mandatory')
digital_sen4_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen4-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen4_1.setStatus('mandatory')
digital_sen4_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen4-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen4_2.setStatus('mandatory')
digital_sen4_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen4-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen4_3.setStatus('mandatory')
digital_sen4_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen4-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen4_4.setStatus('mandatory')
digital_sen4_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen4-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen4_5.setStatus('mandatory')
digital_sen4_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen4-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen4_6.setStatus('mandatory')
digital_sen4_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 4, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen4-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen4_7.setStatus('mandatory')
digital_sen5_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen5-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen5_1.setStatus('mandatory')
digital_sen5_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen5-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen5_2.setStatus('mandatory')
digital_sen5_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen5-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen5_3.setStatus('mandatory')
digital_sen5_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen5-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen5_4.setStatus('mandatory')
digital_sen5_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen5-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen5_5.setStatus('mandatory')
digital_sen5_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen5-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen5_6.setStatus('mandatory')
digital_sen5_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 5, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen5-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen5_7.setStatus('mandatory')
digital_sen6_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen6-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen6_1.setStatus('mandatory')
digital_sen6_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen6-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen6_2.setStatus('mandatory')
digital_sen6_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen6-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen6_3.setStatus('mandatory')
digital_sen6_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen6-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen6_4.setStatus('mandatory')
digital_sen6_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen6-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen6_5.setStatus('mandatory')
digital_sen6_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen6-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen6_6.setStatus('mandatory')
digital_sen6_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 6, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen6-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen6_7.setStatus('mandatory')
digital_sen7_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen7-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen7_1.setStatus('mandatory')
digital_sen7_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen7-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen7_2.setStatus('mandatory')
digital_sen7_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen7-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen7_3.setStatus('mandatory')
digital_sen7_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen7-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen7_4.setStatus('mandatory')
digital_sen7_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen7-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen7_5.setStatus('mandatory')
digital_sen7_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen7-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen7_6.setStatus('mandatory')
digital_sen7_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 7, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen7-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen7_7.setStatus('mandatory')
digital_sen8_1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen8-1").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen8_1.setStatus('mandatory')
digital_sen8_2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen8-2").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen8_2.setStatus('mandatory')
digital_sen8_3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen8-3").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen8_3.setStatus('mandatory')
digital_sen8_4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen8-4").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen8_4.setStatus('mandatory')
digital_sen8_5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen8-5").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen8_5.setStatus('mandatory')
digital_sen8_6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen8-6").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen8_6.setStatus('mandatory')
digital_sen8_7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 2, 8, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setLabel("digital-sen8-7").setMaxAccess("readonly")
if mibBuilder.loadTexts: digital_sen8_7.setStatus('mandatory')
switch_sen1 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen1").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen1.setStatus('mandatory')
switch_sen2 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen2").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen2.setStatus('mandatory')
switch_sen3 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen3").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen3.setStatus('mandatory')
switch_sen4 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen4").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen4.setStatus('mandatory')
switch_sen5 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen5").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen5.setStatus('mandatory')
switch_sen6 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen6").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen6.setStatus('mandatory')
switch_sen7 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen7").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen7.setStatus('mandatory')
switch_sen8 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen8").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen8.setStatus('mandatory')
switch_sen9 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen9").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen9.setStatus('mandatory')
switch_sen10 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen10").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen10.setStatus('mandatory')
switch_sen11 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen11").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen11.setStatus('mandatory')
switch_sen12 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen12").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen12.setStatus('mandatory')
switch_sen13 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen13").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen13.setStatus('mandatory')
switch_sen14 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen14").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen14.setStatus('mandatory')
switch_sen15 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen15").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen15.setStatus('mandatory')
switch_sen16 = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 1, 3, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("switch-sen16").setMaxAccess("readonly")
if mibBuilder.loadTexts: switch_sen16.setStatus('mandatory')
alarmmessage = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 2, 1), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: alarmmessage.setStatus('mandatory')
externalrelay1_element_one = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-one").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_one.setStatus('mandatory')
externalrelay1_element_two = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-two").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_two.setStatus('mandatory')
externalrelay1_element_three = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-three").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_three.setStatus('mandatory')
externalrelay1_element_four = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-four").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_four.setStatus('mandatory')
externalrelay1_element_five = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-five").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_five.setStatus('mandatory')
externalrelay1_element_six = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-six").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_six.setStatus('mandatory')
externalrelay1_element_seven = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-seven").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_seven.setStatus('mandatory')
externalrelay1_element_eight = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay1-element-eight").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay1_element_eight.setStatus('mandatory')
externalrelay2_element_one = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-one").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_one.setStatus('mandatory')
externalrelay2_element_two = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-two").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_two.setStatus('mandatory')
externalrelay2_element_three = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-three").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_three.setStatus('mandatory')
externalrelay2_element_four = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-four").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_four.setStatus('mandatory')
externalrelay2_element_five = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-five").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_five.setStatus('mandatory')
externalrelay2_element_six = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-six").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_six.setStatus('mandatory')
externalrelay2_element_seven = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-seven").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_seven.setStatus('mandatory')
externalrelay2_element_eight = MibScalar((1, 3, 6, 1, 4, 1, 20916, 1, 11, 3, 2, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 1))).setLabel("externalrelay2-element-eight").setMaxAccess("readwrite")
if mibBuilder.loadTexts: externalrelay2_element_eight.setStatus('mandatory')
mibBuilder.exportSymbols("ROOMALERT32S-MIB", internal_tempc=internal_tempc, digital_sen4_7=digital_sen4_7, digital_sen7_5=digital_sen7_5, digital_sen8_4=digital_sen8_4, digital_sen3_6=digital_sen3_6, roomalert32S=roomalert32S, externalrelays=externalrelays, temperature=temperature, internal_heat_index=internal_heat_index, digital_sen8_2=digital_sen8_2, switch_sen4=switch_sen4, externalrelay1_element_two=externalrelay1_element_two, relay=relay, digital_sen2_7=digital_sen2_7, products=products, digital_sen7=digital_sen7, dew_point=dew_point, digital_sen2_2=digital_sen2_2, digital_sen8_6=digital_sen8_6, internal=internal, digital_sen6_1=digital_sen6_1, externalrelay2_element_four=externalrelay2_element_four, digital_sen5_7=digital_sen5_7, sensors=sensors, digital_sen8_1=digital_sen8_1, externalrelay2_element_one=externalrelay2_element_one, switch_sen6=switch_sen6, digital_sen6_7=digital_sen6_7, digital_sen4_6=digital_sen4_6, digital_sen5_4=digital_sen5_4, analog=analog, digital_sen5_3=digital_sen5_3, internal_dew_point_c=internal_dew_point_c, digital_sen5=digital_sen5, avtech=avtech, digital_sen6_4=digital_sen6_4, digital_sen8_3=digital_sen8_3, digital_sen8_5=digital_sen8_5, internal_analog1=internal_analog1, digital_sen4_5=digital_sen4_5, externalrelay2_element_five=externalrelay2_element_five, digital_sen5_6=digital_sen5_6, externalrelay1=externalrelay1, switch_sen9=switch_sen9, switch_sen5=switch_sen5, digital_sen8=digital_sen8, digital_sen3=digital_sen3, traps=traps, externalrelay1_element_one=externalrelay1_element_one, switch_sen16=switch_sen16, digital_sen1_2=digital_sen1_2, digital_sen5_5=digital_sen5_5, externalrelay1_element_three=externalrelay1_element_three, switch_sen10=switch_sen10, externalrelay1_element_five=externalrelay1_element_five, externalrelay2=externalrelay2, digital_sen7_4=digital_sen7_4, digital_sen1_1=digital_sen1_1, externalrelay2_element_eight=externalrelay2_element_eight, digital_sen1_6=digital_sen1_6, switch_sen14=switch_sen14, externalrelay1_element_seven=externalrelay1_element_seven, digital_sen7_7=digital_sen7_7, digital_sen3_7=digital_sen3_7, digital_sen1_3=digital_sen1_3, internal_heat_indexC=internal_heat_indexC, digital_sen6_2=digital_sen6_2, digital_sen7_2=digital_sen7_2, switch_sen2=switch_sen2, heat_index=heat_index, internal_dew_point_f=internal_dew_point_f, switch=switch, switch_sen12=switch_sen12, externalrelay1_element_eight=externalrelay1_element_eight, digital_sen2_4=digital_sen2_4, internal_analog2=internal_analog2, externalrelay1_element_four=externalrelay1_element_four, digital_sen2_3=digital_sen2_3, internal_humidity=internal_humidity, internal_relay1=internal_relay1, switch_sen8=switch_sen8, switch_sen13=switch_sen13, digital_sen5_1=digital_sen5_1, switch_sen15=switch_sen15, externalrelay2_element_two=externalrelay2_element_two, digital_sen3_1=digital_sen3_1, switch_sen11=switch_sen11, digital_sen2_6=digital_sen2_6, digital_sen1=digital_sen1, digital_sen6_3=digital_sen6_3, digital_sen1_5=digital_sen1_5, digital_sen5_2=digital_sen5_2, switch_sen3=switch_sen3, digital_sen4_2=digital_sen4_2, internal_tempf=internal_tempf, digital_sen6_5=digital_sen6_5, switch_sen7=switch_sen7, externalrelay2_element_six=externalrelay2_element_six, digital_sen7_6=digital_sen7_6, internal_power=internal_power, digital_sen7_1=digital_sen7_1, digital_sen4_1=digital_sen4_1, switch_sen1=switch_sen1, digital_sen8_7=digital_sen8_7, digital_sen2_5=digital_sen2_5, power=power, digital_sen1_4=digital_sen1_4, externalrelay2_element_seven=externalrelay2_element_seven, digital=digital, humidity=humidity, digital_sen2_1=digital_sen2_1, digital_sen4=digital_sen4, externalrelay1_element_six=externalrelay1_element_six, digital_sen6_6=digital_sen6_6, externalrelay2_element_three=externalrelay2_element_three, alarmmessage=alarmmessage, digital_sen6=digital_sen6, digital_sen3_5=digital_sen3_5, digital_sen4_4=digital_sen4_4, digital_sen3_3=digital_sen3_3, digital_sen2=digital_sen2, digital_sen3_4=digital_sen3_4, digital_sen4_3=digital_sen4_3, digital_sen1_7=digital_sen1_7, digital_sen7_3=digital_sen7_3, digital_sen3_2=digital_sen3_2, internal_relay2=internal_relay2)
