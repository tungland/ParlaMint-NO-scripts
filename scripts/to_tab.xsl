<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" indent="yes"/>
    <xsl:strip-space elements="*"/>
<!-- Convert parlamint xml to csv with segments -->

    <xsl:template match="/">
    <!-- <xsl:for-each select="*:TEI/*/text/*:body/*:div/*:u/*:seg"> -->
    <xsl:for-each select="*:TEI/*:text/*:body/*:div/*:u/*:seg">
    <!-- <xsl:copy-of select="."></xsl:copy-of> -->
    <xsl:call-template name="segment"></xsl:call-template>

</xsl:for-each>

</xsl:template>
<xsl:template name="segment">
    <xsl:value-of select="@xml:id"></xsl:value-of>
    <xsl:text>&#9;</xsl:text>
    <xsl:value-of select="."/>
    <xsl:text>&#xa;</xsl:text>

</xsl:template>

    </xsl:stylesheet>