<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <!-- <xsl:output method="text"/> -->
    <xsl:strip-space elements="*"/>

    <xsl:template match="node()[not(self::Merknad)]">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="Merknad">
        <xsl:if test="contains(., 'presidentplassen')">
            <xsl:copy-of select="."/>
        </xsl:if>
    </xsl:template>




</xsl:stylesheet>