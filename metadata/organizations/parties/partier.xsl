<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:st="http://data.stortinget.no">
    <xsl:output method="xml"/>
    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
        <parti_liste>
            <xsl:for-each select='st:partier_oversikt/st:partier_liste/st:parti'>
                <xsl:call-template name="parti"/>
            </xsl:for-each>
        </parti_liste>
    </xsl:template>

    <xsl:template name="parti">
        <xsl:variable name="ab" select="upper-case(st:id)"></xsl:variable>
        <org xml:id="party.{$ab}" role="politicalParty">
            <orgName full="yes" xml:lang="no">
                <xsl:value-of select="st:navn"/>
            </orgName>
            <orgName full="init" xml:lang="no">
                <xsl:value-of select="st:id"/>
            </orgName>
        </org>
    </xsl:template>
</xsl:stylesheet>